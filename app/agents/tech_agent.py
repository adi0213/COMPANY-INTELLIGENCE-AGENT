from app.agents.base_agent import BaseAgent

class TechAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TechStackAgent",
            role_description="Specialist in software engineering, programming languages, cloud infrastructure, and AI technologies."
        )

    def get_domain_filter(self) -> str:
        return "technology stack, programming languages, frameworks, cloud infrastructure, artificial intelligence, engineering"
