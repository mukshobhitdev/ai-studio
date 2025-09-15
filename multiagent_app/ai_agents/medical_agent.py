import os
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from tools import medical_tools

load_dotenv(override=True)


DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)


medical_agent = Agent(
    name="MedicalAgent",
    instructions=(
        "You are MedicalAgent. Provide only general medical information and education. "
        "Always include a clear disclaimer that your responses are not medical advice and cannot replace consultation with a qualified healthcare professional. "
        "Encourage users to see a clinician for diagnosis or treatment. "
        "Use your tools to check symptoms or provide lab reference information. "
        "If the request is unclear or outside your scope, ask for clarification or advise seeing a clinician."
    ),
    tools=[medical_tools.symptom_checker, medical_tools.lab_reference],
    model=model
)
