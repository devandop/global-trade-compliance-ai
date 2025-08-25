import streamlit as st
import requests
import uuid
import json
import os

st.set_page_config(page_title="Global Trade & Compliance AI", layout="wide")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def login(username, password):
    try:
        response = requests.post(f"{BACKEND_URL}/token", data={"username": username, "password": password})
        response.raise_for_status()
        st.session_state.auth_token = response.json()['access_token']
        st.session_state.logged_in = True
        st.experimental_rerun()
    except requests.exceptions.HTTPError as e:
        st.error(f"Login failed: {e.response.json().get('detail', 'Incorrect username or password')}")

def signup(username, password):
    try:
        response = requests.post(f"{BACKEND_URL}/signup", json={"username": username, "password": password})
        response.raise_for_status()
        st.success("Signup successful! Please log in.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Signup failed: {e.response.json().get('detail', 'Username may already be taken')}")

def show_login_page():
    st.title("Welcome to the Compliance AI Assistant")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        signup_button = st.form_submit_button("Signup")
        
        if login_button:
            login(username, password)
        if signup_button:
            signup(username, password)

def show_chat_page():
    st.title("🌍 Global Trade & Compliance AI Assistant")
    if st.button("Logout"):
        del st.session_state.auth_token
        del st.session_state.logged_in
        st.experimental_rerun()

    if "messages" not in st.session_state: st.session_state.messages = []
    if "session_id" not in st.session_state: st.session_state.session_id = str(uuid.uuid4())
    if "flow_paused_for_action" not in st.session_state: st.session_state.flow_paused_for_action = False

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Ask a compliance question..."):
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
                else:
                    assistant_message = data.get('message', 'An unknown error occurred.')

                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                with st.chat_message("assistant"): st.markdown(assistant_message, unsafe_allow_html=True)
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to backend: {e}")

# --- Main App Router ---
if st.session_state.get('logged_in', False):
    show_chat_page()
else:
    show_login_page()
