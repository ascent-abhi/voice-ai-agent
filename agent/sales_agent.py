from agent.steps import AgentStep
from models.lead import Lead


class SalesAgent:
    def __init__(self):
        self.step = AgentStep.INTRO
        self.memory = []
        self.lead = Lead()

    def get_next_prompt(self):
        if self.step == AgentStep.INTRO:
            self.step = AgentStep.PAIN
            return (
                "Hi, this is Alex from XYZ Solutions. "
                "You recently showed interest in improving sales productivity. "
                "I’d love to understand your current challenges."
            )

        if self.step == AgentStep.PAIN:
            return "What's the biggest challenge you're facing in your sales process?"

        if self.step == AgentStep.TOOL:
            return "What tools or software are you currently using for sales?"

        if self.step == AgentStep.AUTHORITY:
            return "Are you involved in making decisions about purchasing sales tools?"

        if self.step == AgentStep.BUDGET:
            return "Do you have a budget allocated for improving sales tools?"

        if self.step == AgentStep.TIMELINE:
            return "What’s your timeline for implementing a solution?"

        if self.step == AgentStep.COMPANY_SIZE:
            return "Roughly how many employees are in your company?"

        return None

    def handle_user_response(self, user_input: str):
        """
        Update lead data and move to the next step
        """
        if self.step == AgentStep.PAIN:
            self.lead.pain_points.append(user_input)
            self.step = AgentStep.TOOL

        elif self.step == AgentStep.TOOL:
            self.lead.current_tool = user_input
            self.step = AgentStep.AUTHORITY

        elif self.step == AgentStep.AUTHORITY:
            self.lead.authority = user_input
            self.step = AgentStep.BUDGET

        elif self.step == AgentStep.BUDGET:
            self.lead.budget = user_input
            self.step = AgentStep.TIMELINE

        elif self.step == AgentStep.TIMELINE:
            self.lead.timeline = user_input
            self.step = AgentStep.COMPANY_SIZE

        elif self.step == AgentStep.COMPANY_SIZE:
            self.lead.company_size = user_input
            self.step = AgentStep.JUDGEMENT
