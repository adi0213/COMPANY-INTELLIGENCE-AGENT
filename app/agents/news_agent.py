from app.agents.base_agent import BaseAgent

class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NewsAgent",
            role_description="Specialist in recent events, product launches, controversies, and press releases."
        )

    def get_domain_filter(self) -> str:
        return "recent news, press releases, announcements, recent events"
