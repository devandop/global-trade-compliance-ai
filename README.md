🌍 Global Trade & Compliance AI Assistant
Welcome to the Global Trade & Compliance AI Assistant, a powerful, intelligent application designed to simplify the complexities of international trade. This tool leverages a sophisticated AI agent, orchestrated by Portia AI, to provide real-time compliance checks, automate financial transactions via Xero, and integrate seamlessly into your business workflows with Slack.
🎯 The Pain Point
Global trade is a minefield of complex, ever-changing regulations. Businesses, especially small to medium-sized enterprises, face significant challenges:
Product Classification: Incorrectly identifying Harmonized System (HS) codes leads to customs delays, fines, and incorrect duty payments.
Sanctions Screening: Manually checking customers against global sanctions lists is time-consuming and prone to human error, carrying severe legal and financial risks.
Duty & Tax Calculation: Calculating accurate landed costs, including duties and taxes for various countries, is a complex and often manual process.
Workflow Inefficiency: Disconnected systems for compliance, accounting (like Xero), and communication (like Slack) lead to manual data entry, delays, and a lack of a unified audit trail.
This AI assistant was built to solve these problems by providing a single, intelligent, conversational interface to manage these critical compliance tasks.
✨ Features
Conversational AI Interface: Interact with the assistant using natural language through a clean, web-based chat UI.
Dynamic AI Planning: Powered by Portia AI, the assistant can understand complex user requests and dynamically generate multi-step plans to achieve them.
Compliance Checks:
HS Code Lookup: Instantly find Harmonized System codes for products.
Sanctions Screening: (Conceptual) Vet entities against global watchlists.
Seamless Xero Integration:
Connects securely to your Xero account.
Fetches real-time data like tax rates for accurate duty calculations.
Creates invoices and other transactions directly in Xero.
Slack for Approvals: For high-value or sensitive operations, the assistant can send approval requests to a designated Slack channel, pausing its workflow until human approval is received.
Secure and Scalable: Built with a production-ready architecture, including secure user authentication, persistent state management, and designed for cloud deployment.
🛠️ Technology Stack
This project uses a modern, robust technology stack to deliver a seamless and powerful user experience.
Component	Technology	Purpose
Frontend	
![alt text](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
For building the interactive web-based chat user interface.
Backend API	
![alt text](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
A high-performance Python framework for building the secure and robust API server.
AI Agent Orchestration	
![alt text](https://img.shields.io/badge/Portia_AI-8A2BE2?style=for-the-badge)
The core platform for orchestrating tools, managing plans, and handling auth flows.
Large Language Model	
![alt text](https://img.shields.io/badge/Google_Gemini-8E75B9?style=for-the-badge&logo=google&logoColor=white)
Provides the natural language understanding and reasoning capabilities for the agent.
Database	
![alt text](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
For persistent storage of user accounts and application data.
Cache & State Store	
![alt text](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
For managing application state, chat history, and idempotency keys.
Financial Integration	
![alt text](https://img.shields.io/badge/Xero-13B5EA?style=for-the-badge&logo=xero&logoColor=white)
Connected via Portia's Local MCP for real-time accounting data and transaction creation.
Workflow Integration	
![alt text](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)
For sending notifications and handling out-of-band human approval steps.
Containerization	
![alt text](https://img.shields.io/badge/docker-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white)
For packaging the backend application and its dependencies for consistent deployment.
Deployment	
![alt text](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
A cloud platform for deploying the backend, database, and Redis services.
📂 Project Directory Structure
The project is organized into distinct components for a clean separation of concerns.
code
Code
global-trade-compliance-ai/
├── backend/                  # FastAPI application, database models, and auth logic
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── redis_client.py
│   ├── database.py
│   ├── models.py
│   └── auth.py
├── frontend/                 # Streamlit UI application
│   ├── app.py
│   └── requirements.txt
├── portia-agent/             # Core AI agent and Portia SDK client logic
│   ├── portia_client.py
│   └── agent.py
├── deployment/               # Deployment artifacts
│   └── Dockerfile
├── .gitignore                # Specifies files and folders for Git to ignore
├── render.yaml               # Render Blueprint for Infrastructure as Code
└── README.md                 # This file
🚀 Getting Started: Setup and Deployment
Prerequisites
Python 3.9+
Node.js v18+ & npm
Docker
Git
A Render account
A Streamlit Cloud account
API Keys from: Google, Portia AI, Xero (Custom Connection), and Tavily.
Local Development Setup
Clone the repository:
code
Bash
git clone <your_repo_url>
cd global-trade-compliance-ai
Create and configure your secrets file:
Copy the template: cp backend/.env.example backend/.env
Edit backend/.env and fill in all your acquired API keys and local database URL.
Run the one-time setup script:
This will create a Python virtual environment and install all dependencies.
code
Bash
chmod +x setup.sh
./setup.sh
Activate the virtual environment and run the application:
code
Bash
source venv/bin/activate
chmod +x run_dev.sh
./run_dev.sh
The FastAPI backend will be available at http://localhost:8000.
The Streamlit frontend will be available at http://localhost:8501.
Production Deployment
This application is designed for a robust deployment on Render and Streamlit Cloud.
Push to GitHub: Commit all project files (except .env) to a private GitHub repository.
Deploy to Render (Backend, DB, Redis):
Create PostgreSQL and Redis instances on your Render dashboard.
Create a "Web Service" for the backend, connecting it to your GitHub repo and selecting the Docker runtime.
In the "Environment" tab, add all the necessary secret keys (e.g., PORTIA_API_KEY, DATABASE_URL, REDIS_URL, etc.) from your .env file. Use the internal connection strings provided by your Render DB and Redis instances.
Deploy to Streamlit Cloud (Frontend):
Create a new app in Streamlit Cloud and connect it to the same GitHub repository.
Set the main file path to frontend/app.py.
In the "Secrets" section, add the BACKEND_URL pointing to your deployed Render backend's public URL.
Note on AI Assistance: This project, including its architecture, code, and documentation, was developed with significant assistance from Google's Gemini (an LLM). It serves as a powerful example of human-AI collaboration in building complex, modern software applications.
