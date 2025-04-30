from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI

from smart_agent import SmartAgentAzure

# Azure setup
client = AzureOpenAI(
    api_key="3defcAl4fWTcgyu5zQo1CV0nxotVoQOY0CkCfpxv5dwhEjf3vp5UJQQJ99BDACHYHv6XJ3w3AAAAACOGe5gy",
    api_version="2024-12-01-preview",
    azure_endpoint="https://krish-m9iq4eev-eastus2.cognitiveservices.azure.com/"
)

agent = SmartAgentAzure(client=client, deployment="gpt-4o-mini")

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/agent")
async def ask_agent(q: Query):
    response = agent.think_and_act(q.question)
    return {"response": response}
