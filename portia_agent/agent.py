# portia-agent/agent.py
import os
import json
import google.generativeai as genai
from portia import PlanRun
from portia_agent.portia_client import PortiaClient
from backend.redis_client import get_redis_client # For managing chat history

class PortiaAIAgent:
    def __init__(self, portia_api_key: str, google_api_key: str, xero_client_id: str, xero_client_secret: str):
        self.portia_client = PortiaClient(portia_api_key, xero_client_id, xero_client_secret)
        self.portia_sdk = self.portia_client.get_sdk()
        
        # Configure the Gemini LLM for the pre-processing step
        genai.configure(api_key=google_api_key)
        self.pre_processing_llm = genai.GenerativeModel('gemini-1.5-flash')
        self.redis = get_redis_client()

    def _get_chat_history(self, session_id: str):
        """Retrieves chat history from Redis."""
        key = f"chat_history:{session_id}"
        # Use Redis's list capabilities for a proper chat log
        history_raw = self.redis.lrange(key, 0, -1)
        # Decode from bytes if necessary, then parse JSON
        return [json.loads(item) for item in history_raw]

    def _save_chat_history(self, session_id: str, user_query: str, assistant_response: str):
        """Saves the latest turn of conversation to Redis."""
        key = f"chat_history:{session_id}"
        # Push user message
        self.redis.rpush(key, json.dumps({"role": "user", "content": user_query}))
        # Push assistant response
        self.redis.rpush(key, json.dumps({"role": "assistant", "content": assistant_response}))
        # Set an expiration time on the chat history
        self.redis.expire(key, 3600) # Expire in 1 hour

    def pre_process_query(self, user_query: str, session_id: str) -> dict:
        """
        Uses Gemini to act as a compliance expert. It checks if the query is complete
        enough to be executed, or if it needs clarification, considering chat history.
        """
        chat_history = self._get_chat_history(session_id)
        
        prompt = f"""
        You are a world-class Global Trade Compliance expert. Your task is to analyze a user's request and determine if it contains all the necessary information to be sent to an execution engine. You must consider the previous conversation for context.

        CRITICAL RULES:
        - If the user asks for an "HS Code", you MUST have a "destination country".
        - If the user asks to "calculate duty", you MUST have a "product description", a "value" with "currency", and a "destination country".
        - If the user asks to "create an invoice", you MUST have a "customer name", "product description", and an "amount" with a "currency".

        Analyze the following user query in the context of our conversation history.

        CONVERSATION HISTORY (last 4 messages):
        {json.dumps(chat_history[-4:])}

        CURRENT USER QUERY: "{user_query}"

        Respond in a single, valid JSON object with one of two formats:

        1. If the query (combined with history) is complete and ready for execution, respond with:
        {{
            "status": "ready_for_execution",
            "enriched_query": "A complete, self-contained query for the execution engine. Example: 'Find the HS code for a wooden chair for import into Germany and then calculate the duty for a value of 150 EUR.'"
        }}

        2. If the query is ambiguous or missing information, respond with:
        {{
            "status": "clarification_needed",
            "clarification_question": "Your expert question to the user to get the missing information. Example: 'I can certainly look that up for you. Which country are you importing the chair into?'"
        }}
        """
        try:
            response = self.pre_processing_llm.generate_content(prompt)
            # Basic cleanup for the LLM response
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            analysis = json.loads(cleaned_response)

            # Save conversation history after successful analysis
            assistant_response = analysis.get("clarification_question", "Okay, I will process that.")
            self._save_chat_history(session_id, user_query, assistant_response)

            return analysis

        except Exception as e:
            print(f"Error during pre-processing: {e}")
            return {"status": "error", "error_message": "Failed to analyze query."}

    def start_new_task(self, enriched_query: str, end_user_id: str) -> PlanRun:
        """
        Generates and runs a plan using Portia's planner.
        This is now only called with an enriched, validated query.
        """
        print(f"Agent: Generating plan for enriched query: '{enriched_query}'")
        plan = self.portia_sdk.plan(enriched_query)
        print(f"Agent: Plan generated. ID: {plan.id}. Starting run for user '{end_user_id}'...")
        plan_run = self.portia_sdk.run_plan(plan, end_user_id=end_user_id)
        print(f"Agent: Plan run started. Initial state: {plan_run.state}")
        return plan_run
