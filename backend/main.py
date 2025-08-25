# backend/main.py

import os
# --- PATH CORRECTION ---
# This code tells Python to add the project's root directory
# to the list of paths it searches for modules.
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --- END PATH CORRECTION ---

import pickle
import json
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Local imports
from portia_agent.agent import PortiaAIAgent
from portia import ActionClarification, InputClarification, MultipleChoiceClarification, PlanRunState, PlanRun
from backend.redis_client import get_redis_client
from backend.database import get_db, Base, engine
from backend.models import User
from backend.auth import create_access_token, get_password_hash, verify_password, get_current_user

# --- Database Setup ---
Base.metadata.create_all(bind=engine)

# --- App Initialization ---
load_dotenv()
app = FastAPI(title="Global Trade Compliance AI Backend")

# --- SECURE CORS CONFIGURATION FOR PRODUCTION ---
allowed_origins = [
    "http://localhost:8501",
    "http://localhost",
]
PRODUCTION_FRONTEND_URL = os.getenv("FRONTEND_URL")
if PRODUCTION_FRONTEND_URL:
    allowed_origins.append(PRODUCTION_FRONTEND_URL)

app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Client Initializations ---
# Pass the GOOGLE_API_KEY for the pre-processing LLM
agent = PortiaAIAgent(
    portia_api_key=os.getenv("PORTIA_API_KEY"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    xero_client_id=os.getenv("XERO_CLIENT_ID"),
    xero_client_secret=os.getenv("XERO_CLIENT_SECRET")
)
redis = get_redis_client()
portia_sdk = agent.portia_client.get_sdk()

# --- HEALTH CHECK ENDPOINT (for Render) ---
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}

# --- Models and Helper Functions ---
class ChatRequest(BaseModel):
    user_message: str
    session_id: str
class UserCreate(BaseModel):
    username: str
    password: str

def store_plan_run(session_id: str, plan_run: PlanRun):
    redis.set(f"plan_run:{session_id}", pickle.dumps(plan_run), ex=3600)
def get_plan_run(session_id: str) -> PlanRun:
    data = redis.get(f"plan_run:{session_id}")
    return pickle.loads(data) if data else None

# --- Authentication Endpoints ---
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Core Application Endpoints (Protected) ---
@app.post("/chat")
def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    end_user_id = str(current_user.id)
    
    # --- NEW PRE-PROCESSING STEP ---
    processed_query = agent.pre_process_query(request.user_message, request.session_id)
    
    if processed_query.get("status") == "clarification_needed":
        return {
            "response_type": "clarification_input",
            "message": processed_query.get("clarification_question")
        }
    
    if processed_query.get("status") == "error":
        raise HTTPException(status_code=500, detail="Failed to pre-process query.")
    # --- END PRE-PROCESSING STEP ---

    # If the query is ready, use the enriched version to start the task
    enriched_query = processed_query.get("enriched_query")
    try:
        plan_run = agent.start_new_task(enriched_query, end_user_id)
        store_plan_run(request.session_id, plan_run)
        
        if plan_run.state == PlanRunState.NEED_CLARIFICATION:
            clarification = plan_run.get_outstanding_clarifications()[0]
            if isinstance(clarification, ActionClarification):
                return {"response_type": "clarification_action", "message": clarification.user_guidance, "action_url": clarification.action_url}
            else:
                return {"response_type": "clarification_input", "message": clarification.user_guidance}
        elif plan_run.state == PlanRunState.DONE:
            return {"response_type": "success", "message": "Task completed instantly!", "result": plan_run.output}
        else:
            return {"response_type": "pending", "message": "Task is in progress..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resume_flow")
def resume_flow(request: ChatRequest, current_user: User = Depends(get_current_user)):
    plan_run = get_plan_run(request.session_id)
    if not plan_run:
        raise HTTPException(status_code=404, detail="No active plan found for this session.")
    
    try:
        # First, try to resolve any outstanding text-based clarifications
        # This handles the case where a user is replying to a question
        needs_resume = True
        if plan_run.state == PlanRunState.NEED_CLARIFICATION:
            clarification = plan_run.get_outstanding_clarifications()[0]
            if isinstance(clarification, InputClarification) or isinstance(clarification, MultipleChoiceClarification):
                plan_run = portia_sdk.resolve_clarification(clarification, request.user_message, plan_run)
                # After resolving, we will still call resume
            elif isinstance(clarification, ActionClarification):
                plan_run = portia_sdk.wait_for_ready(plan_run)
                # After waiting, we might not need to resume if it's DONE
                if plan_run.state == PlanRunState.DONE:
                    needs_resume = False
        
        # If the plan is not done, resume it
        if needs_resume and plan_run.state != PlanRunState.DONE:
            plan_run = portia_sdk.resume(plan_run)

        store_plan_run(request.session_id, plan_run)

        if plan_run.state == PlanRunState.DONE:
            return {"response_type": "success", "message": "Task completed!", "result": plan_run.output}
        elif plan_run.state == PlanRunState.NEED_CLARIFICATION:
            new_clarification = plan_run.get_outstanding_clarifications()[0]
            return {"response_type": "clarification_input", "message": new_clarification.user_guidance}
        else:
            return {"response_type": "pending", "message": "Task is still in progress..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Note: The startup event for plan registration is removed as the new
#       design dynamically generates plans with `portia.plan()`.
#       If you want to keep pre-defined plans, you can add the startup event back
#       and modify the agent to use those plan IDs instead of dynamic generation.
