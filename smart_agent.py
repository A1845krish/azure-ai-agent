from openai import AzureOpenAI


TOOL_PROMPTS = {
    "calculator": "You are a calculator. Solve the math expression given.",
    "unit_converter": "You are a unit converter. Convert units (e.g., meters to feet).",
    "date_difference": "You are a date calculator. Calculate the number of days between two dates.",
    "none": "You are a polite assistant. Explain that the request is out of your scope."
}


class SmartAgentAzure:
    def __init__(self, client, deployment):
        self.client = client
        self.deployment = deployment

    def choose_tool(self, user_input):
        tool_prompt = f"""
You are an AI reasoning agent with access to these tools:
- calculator: for basic math (add, subtract, multiply, divide)
- unit_converter: for converting units like meters to feet
- date_difference: for calculating number of days between dates

User input: "{user_input}"

Which tool should be used? Reply with only one of: calculator, unit_converter, date_difference, or none.
"""
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "You are a helpful reasoning assistant."},
                {"role": "user", "content": tool_prompt}
            ]
        )
        return response.choices[0].message.content.strip().lower()

    def use_tool(self, tool_name, user_input):
        role_description = TOOL_PROMPTS.get(tool_name, TOOL_PROMPTS["none"])

        tool_response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": role_description},
                {"role": "user", "content": user_input}
            ]
        )
        return tool_response.choices[0].message.content.strip()

    def think_and_act(self, user_input):
        tool = self.choose_tool(user_input)
        return self.use_tool(tool, user_input)

