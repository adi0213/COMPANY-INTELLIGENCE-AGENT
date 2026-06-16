from app.agents.base_agent import BaseAgent

class CompanyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CompanyOverviewAgent",
            role_description="Specialist in corporate history, leadership, and overall business models."
        )

    def get_domain_filter(self) -> str:
        return "company overview, history, founders, business model, executives"
