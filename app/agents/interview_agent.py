from app.agents.base_agent import BaseAgent

class InterviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="InterviewPrepAgent",
            role_description="Specialist in interview questions, LeetCode patterns, behavioral rounds, and hiring culture."
        )

    def get_domain_filter(self) -> str:
        return "interview questions, hiring process, behavioral interview, technical interview, coding rounds"
