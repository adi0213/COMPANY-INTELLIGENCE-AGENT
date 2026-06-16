from app.agents.base_agent import BaseAgent

class HiringAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="HiringTrendsAgent",
            role_description="Specialist in job market trends, open roles, remote work policies, and employee growth."
        )

    def get_domain_filter(self) -> str:
        return "hiring trends, job openings, recruitment, careers, remote work"
