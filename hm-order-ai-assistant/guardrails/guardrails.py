
# Guardrail logic for validating if a user query can be served by available agents
from agents import Agent, Runner, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem, input_guardrail, OpenAIChatCompletionsModel
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

class FalseQueryGuardrailOutput(BaseModel):
    is_false: bool
    reason: str

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model = OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

# Make sure these agent names match your actual agent identifiers
AVAILABLE_AGENTS = [
    "ResearchAgent",
    "DocAgent",
    "MedicalAgent",
    "StocksAgent",
    "TravelAgent"
]

false_query_guardrail_agent = Agent(
    name="False Query Guardrail Agent",
    instructions=(
        "Determine if the user's query cannot be served by the available agents. "
        f"Available agents: {', '.join(AVAILABLE_AGENTS)}."
    ),
    model=model,
    output_type=FalseQueryGuardrailOutput
)

@input_guardrail
async def false_query_guardrail(
    context: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """
    Guardrail to check if the user query can be served by any available agent.
    """
    result = await Runner.run(false_query_guardrail_agent, input)
    return GuardrailFunctionOutput(
        tripwire_triggered=result.final_output.is_false,
        output_info=result.final_output
    )

