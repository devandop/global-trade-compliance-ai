import streamlit as st
import requests
import uuid
import json
import os

# --- Page and Backend Configuration ---
st.set_page_config(page_title="Global Trade & Compliance AI", layout="wide")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


# --- Authentication Functions ---
def login(username, password):
    """Handles the login request to the backend."""
    try:
        response = requests.post(f"{BACKEND_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.auth_token = response.json()['access_token']
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error(f"Login failed: {response.json().get('detail', 'Incorrect username or password')}")
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the backend server running?")
    except Exception as e:
        st.error(f"An unexpected error occurred during login: {e}")

def signup(username, password):
    """Handles the signup request to the backend."""
    try:
        response = requests.post(f"{BACKEND_URL}/signup", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Signup successful! Please log in.")
        else:
            st.error(f"Signup failed: {response.json().get('detail', 'Username may already be taken')}")
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the backend server running?")
    except Exception as e:
        st.error(f"An unexpected error occurred during signup: {e}")


# --- UI Views ---
def show_login_page():
    """Displays the login and signup forms."""
    st.title("Welcome to the Compliance AI Assistant")
    
    # --- Login Form ---
    with st.form("login_form"):
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        login_button = st.form_submit_button("Login")
        if login_button:
            login(login_username, login_password)
    
    # --- Signup Form ---
    with st.form("signup_form"):
        st.subheader("Create an Account")
        new_username = st.text_input("New Username", key="signup_user")
        new_password = st.text_input("New Password", type="password", key="signup_pass")
        signup_button = st.form_submit_button("Signup")
        if signup_button:
            signup(new_username, new_password)

def show_chat_page():
    """Displays the main chat interface for logged-in users."""
    st.sidebar.title("Compliance AI")
    if st.sidebar.button("Logout"):
        # A more robust logout that clears the entire session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    st.title("🌍 Global Trade & Compliance AI Assistant")

    # Initialize chat-specific session state
    if "messages" not in st.session_state: st.session_state.messages = []
    if "session_id" not in st.session_state: st.session_state.session_id = str(uuid.uuid4())
    if "flow_paused_for_action" not in st.session_state: st.session_state.flow_paused_for_action = False

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Handle new user input
    if prompt := st.chat_input("Ask a compliance question or give a command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.spinner("Thinking..."):
            endpoint = "/resume_flow" if st.session_state.flow_paused_for_action else "/chat"
            st.session_state.flow_paused_for_action = False
            
            headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
            try:
                response = requests.post(
                    f"{BACKEND_URL}{endpoint}",
                    json={"user_message": prompt, "session_id": st.session_state.session_id},
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                assistant_message = ""
                if data.get("response_type") == "clarification_action":
                    assistant_message = f"{data['message']}\n\nPlease complete the action at this URL, then return here and type 'ok' to continue:\n\n**[Click here to authorize]({data['action_url']})**"
                    st.session_state.flow_paused_for_action = True
                elif data.get("response_type") == "success":
                    result_text = json.dumps(data.get('result'), indent=2)
                    assistant_message = f"{data['message']}\n\n```json\n{result_text}\n```"
                else: # Covers clarification_input, pending, and error types
                    assistant_message = data.get('message', 'An unknown error occurred.')

                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                with st.chat_message("assistant"): st.markdown(assistant_message, unsafe_allow_html=True)

            except requests.exceptions.HTTPError as e:
                error_detail = e.response.json().get("detail", "An unknown error occurred.")
                st.error(f"An error occurred with the backend: {error_detail}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {error_detail}"})
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend: {e}")
                st.session_state.messages.append({"role": "assistant", "content": "Error: Could not connect to the backend."})


# --- Main Application Router ---
# This checks if the user is logged in and shows the appropriate page.
if st.session_state.get('logged_in', False):
    show_chat_page()
else:
    show_login_page()
