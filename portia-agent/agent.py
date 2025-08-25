from portia_agent.portia_client import PortiaClient
from portia import PlanRun

class PortiaAIAgent:
    def __init__(self, portia_api_key: str, xero_client_id: str, xero_client_secret: str):
        self.portia_client = PortiaClient(
            portia_api_key=portia_api_key,
            xero_client_id=xero_client_id,
            xero_client_secret=xero_client_secret
        )
        self.portia_sdk = self.portia_client.get_sdk()

    def start_new_task(self, user_query: str, end_user_id: str) -> PlanRun:
        print(f"Agent: Generating plan for query: '{user_query}'")
        plan = self.portia_sdk.plan(user_query)
        print(f"Agent: Plan generated. ID: {plan.id}. Starting run for user '{end_user_id}'...")
        plan_run = self.portia_sdk.run_plan(plan, end_user_id=end_user_id)
        print(f"Agent: Plan run started. Initial state: {plan_run.state}")
        return plan_run
