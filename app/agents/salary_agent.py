from app.agents.base_agent import BaseAgent

class SalaryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SalaryInsightsAgent",
            role_description="Specialist in compensation, bonuses, equity (RSUs), and benefits."
        )

    def get_domain_filter(self) -> str:
        return "salary, compensation, base pay, bonus, stock options, RSUs, benefits"
