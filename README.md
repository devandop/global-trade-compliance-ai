
# 🌍 Global Trade & Compliance AI Assistant
Welcome to the Global Trade & Compliance AI Assistant, a powerful, intelligent application designed to simplify the complexities of international trade. This tool leverages a sophisticated AI agent, orchestrated by Portia AI, to provide real-time compliance checks, automate financial transactions via Xero, and integrate seamlessly into your business workflows with Slack.
## 🎯 The Pain Point
Global trade is a minefield of complex, ever-changing regulations. Businesses, especially small to medium-sized enterprises, face significant challenges:
- **Product Classification:** Incorrectly identifying Harmonized System (HS) codes leads to customs delays, fines, and incorrect duty payments.
- **Sanctions Screening:** Manually checking customers against global sanctions lists is time-consuming and prone to human error, carrying severe legal and financial risks.
- **Duty & Tax Calculation:** Calculating accurate landed costs, including duties and taxes for various countries, is a complex and often manual process.
- **Workflow Inefficiency:** Disconnected systems for compliance, accounting (like Xero), and communication (like Slack) lead to manual data entry, delays, and a lack of a unified audit trail.
This AI assistant was built to solve these problems by providing a single, intelligent, conversational interface to manage these critical compliance tasks.
## ✨ Features
- **Conversational AI Interface:** Interact with the assistant using natural language through a clean, web-based chat UI.
- **Dynamic AI Planning:** Powered by Portia AI, the assistant can understand complex user requests and dynamically generate multi-step plans to achieve them.
- **Compliance Checks:**
  - HS Code Lookup: Instantly find Harmonized System codes for products.
  - Sanctions Screening: (Conceptual) Vet entities against global watchlists.
- **Seamless Xero Integration:**
    - Connects securely to your Xero account.
    - Fetches real-time data like tax rates for accurate duty calculations.
    - Creates invoices and other transactions directly in Xero.
- **Slack for Approvals:** For high-value or sensitive operations, the assistant can send approval requests to a designated Slack channel, pausing its workflow until human approval is received.
- **Secure and Scalable:** Built with a production-ready architecture, including secure user authentication, persistent state management, and designed for cloud deployment.
## 🛠️ Technology Stack

This project uses a modern, robust technology stack to deliver a seamless and powerful user experience.

| Component                  | Technology                                                                                                    | Purpose                                                                                |
| :------------------------- | :------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------- |
| **Frontend**               | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) | For building the interactive web-based chat user interface.                            |
| **Backend API**            | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)                        | A high-performance Python framework for building the secure and robust API server.     |
| **AI Agent Orchestration** | ![Portia AI](https://img.shields.io/badge/Portia_AI-8A2BE2?style=for-the-badge)                               | The core platform for orchestrating tools, managing plans, and handling auth flows.    |
| **Large Language Model**   | ![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B9?style=for-the-badge&logo=google&logoColor=white) | Provides the natural language understanding and reasoning capabilities for the agent.   |
| **Database**               | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) | For persistent storage of user accounts and application data.                          |
| **Cache & State Store**    | ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)      | For managing application state, chat history, and idempotency keys.                    |
| **Financial Integration**  | ![Xero](https://img.shields.io/badge/Xero-13B5EA?style=for-the-badge&logo=xero&logoColor=white)                 | Connected via Portia's Local MCP for real-time accounting data and transaction creation. |
| **Workflow Integration**   | ![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)              | For sending notifications and handling out-of-band human approval steps.               |
| **Containerization**       | ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white)   | For packaging the backend application and its dependencies for consistent deployment.  |
| **Deployment**             | ![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)           | A cloud platform for deploying the backend, database, and Redis services.              |

## 📂 Project Directory Structure

The project is organized into distinct components for a clean separation of concerns.

```bash
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


---

### 🚀 Getting Started: Setup and Deployment

This section provides a step-by-step guide to set up the project locally and deploy it to production.

#### Prerequisites

Before you begin, ensure you have the following software and accounts:
- **Python 3.9+** installed on your system.
- **Node.js v18+ and npm** installed (required for the Xero MCP Server).
- **Docker** installed and running.
- **Git** installed.
- An account on [Render](https://render.com/).
- An account on [Streamlit Cloud](https://share.streamlit.io/).
- **API Keys** from:
    - Google (for Gemini LLM)
    - Portia AI
    - Xero (create a Custom Connection App)
    - Tavily

#### Local Development Setup

Follow these steps to get the application running on your local Ubuntu WSL environment.

1.  **Clone the repository:**
    ```bash
    # Navigate to where you want to store the project
    # For example, your home directory:
    cd ~ 
    
    # Clone your project from GitHub
    git clone <your_github_repository_url>
    cd global-trade-compliance-ai
    ```

2.  **Create and configure your secrets file:**
    *   Copy the template for backend secrets: `cp backend/.env.example backend/.env`
    *   Edit `backend/.env` and fill in all your acquired API keys (`PORTIA_API_KEY`, `GOOGLE_API_KEY`, `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET`, `TAVILY_API_KEY`) and your local database connection string (`REDIS_URL`, `DATABASE_URL`). You'll also need your `SECRET_KEY` for JWT.

3.  **Make scripts executable and run setup:**
    This crucial step creates the Python virtual environment and installs all project dependencies.
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
    *(Ensure `setup.sh` completed without errors.)*

4.  **Activate the virtual environment and run the application:**
    ```bash
    source venv/bin/activate
    chmod +x run_dev.sh
    ./run_dev.sh
    ```
    After this, the FastAPI backend should be running at `http://localhost:8000`, and the Streamlit frontend at `http://localhost:8501`. Your terminal will be occupied by these running processes.

#### **Production Deployment**

This application is designed for a robust deployment on Render (for backend, database, Redis) and Streamlit Cloud (for frontend).

1.  **Push Code to GitHub:**
    Commit all your project files (especially the correct `backend/requirements.txt`, `frontend/requirements.txt`, `portia-agent/`, `backend/main.py`, `frontend/app.py`, and `deployment/Dockerfile`) to a **private** GitHub repository. Make sure your `.gitignore` file is correctly configured to exclude `.env` files.

2.  **Deploy Data Services and Backend to Render:**
    *   **Create PostgreSQL Instance:** In your Render dashboard -> New -> PostgreSQL. Name it (e.g., `compliance-db`). Copy its **Internal Connection String**.
    *   **Create Redis Instance:** In Render dashboard -> New -> Redis. Name it (e.g., `compliance-redis`). Copy its **Internal Connection URL**.
    *   **Create Backend Web Service:**
        *   New -> Web Service. Connect your GitHub repository.
        *   **Runtime:** Select `Docker`.
        *   **Dockerfile Path:** `./deployment/Dockerfile` (this tells Render to use your Dockerfile to build the image).
        *   **Environment Variables (Secrets):** Add all the necessary secrets here.
            *   `PORTIA_API_KEY`, `GOOGLE_API_KEY`, `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET`, `TAVILY_API_KEY`, `SECRET_KEY` (from your local `.env` file).
            *   `DATABASE_URL`: Paste the Internal Connection String from your Render PostgreSQL instance.
            *   `REDIS_URL`: Paste the Internal Connection URL from your Render Redis instance.
            *   `FRONTEND_URL`: This is important. You will get this URL after deploying the Streamlit frontend. For now, you can use a placeholder or `http://localhost:8501` (it will be updated later).
        *   Deploy the backend service. Once it's live, **copy its public URL** (e.g., `https://compliance-ai-backend.onrender.com`).

3.  **Deploy Frontend to Streamlit Cloud:**
    *   Log in to [Streamlit Cloud](https://share.streamlit.io/).
    *   Click "New app".
    *   Select your GitHub repository.
    *   **Main file path:** `frontend/app.py`.
    *   **App URL:** Choose a unique URL (e.g., `your-app-name`).
    *   **Advanced settings... -> Secrets:** Add the following secret:
        ```
        BACKEND_URL = "YOUR_RENDER_BACKEND_PUBLIC_URL"
        ```
        (Replace `YOUR_RENDER_BACKEND_PUBLIC_URL` with the actual public URL you copied from your Render backend service).
    *   Deploy the Streamlit app.

4.  **Update Render Backend with Frontend URL:**
    *   Go back to your Render dashboard, find your backend service (`compliance-ai-backend`).
    *   Navigate to its **Environment** settings.
    *   Edit the `FRONTEND_URL` environment variable and paste the public URL of your deployed Streamlit Cloud app.
    *   Save changes. Render will redeploy the backend with this updated URL.

---

This structure provides a clean separation between your project's codebase and its deployment instructions, making it clear what needs to be done at each stage.

**Note:**
*   Ensure you have correctly set up your Xero Custom Connection and obtained `XERO_CLIENT_ID`/`XERO_CLIENT_SECRET`.
*   Ensure your Portia AI dashboard is configured with your `PORTIA_API_KEY` and `TAVILY_API_KEY`.
*   The `run_dev.sh` script is for local development only. Render handles the start commands based on the `Dockerfile` and `render.yaml`.


## **Note on AI Assistance:**
 This project, including its architecture, code, and documentation, was developed with significant assistance from Google's Gemini (an LLM). It serves as a powerful example of human-AI collaboration in building complex, modern software applications.
