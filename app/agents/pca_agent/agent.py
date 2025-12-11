"""Root agent module."""

from google.genai import types
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from google.adk.models.lite_llm import LiteLlm

from .prompts import PCA_PROMPT

from app.tools.tools import get_context_from_rag

from app.commons.core import *  # noqa: F403
from app.commons.core import logger
from app.commons.settings import APP_NAME, AGENT_LABELS



OLLAMA_MODEL = "gpt-oss:latest"

model = LiteLlm(model=f"openai/{OLLAMA_MODEL}") 

def create_root_agent():
    agent = Agent(
        name=APP_NAME,
        # model=LiteLlm(model="ollama_chat/llama3:latest"),
        model=model,
        description=(
            "Um ACP - um Agente Conversacional Pedagógico especializado em ajudar estudantes com dúvidas relacionadas a conteúdos acadêmicos."
            "Busca contextos em RAG antes de responder."
        ),
        instruction=PCA_PROMPT,
        tools=[
            get_context_from_rag,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        ],
        generate_content_config=types.GenerateContentConfig(
            labels=AGENT_LABELS,
        ),
    )

    logger.info("Root agent created successfully.")
    return agent


def get_root_agent():
    logger.debug("Getting root agent...")
    return create_root_agent()


root_agent = get_root_agent()
