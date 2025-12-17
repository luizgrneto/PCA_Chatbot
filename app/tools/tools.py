import json
import random
from typing import Dict, Optional

from datetime import datetime

from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

from src.vectorstore.hybrid_vector_store import HybridVectorStore
from src.config.settings import settings


def get_current_date() -> dict:
    """
    Get the current date in the format YYYY-MM-DD
    """
    return {"current_date": datetime.now().strftime("%Y-%m-%d")}

def get_context_from_rag(question: str) -> str:
    """Recupera documentos importantes em forma de contexto, baseado em uma pergunta."""

    store = HybridVectorStore(
        persist_path=settings.DATA_DB,
        embedding_model=settings.EMBEDDING_MODEL
        )

    docs = store.hybrid_search(question, top_k=5)
    context = "\n\n".join([d[1] for d in docs])

    return context

def get_topic_from_json(
    difficulty: str,
    tool_context: ToolContext,
) -> Optional[Dict]:
    """
    ADK tool that returns a non-repeating topic from a JSON dataset
    based on the user's current difficulty level.
    """

    # Initialize session state if missing
    used_topics = tool_context.state.get("used_topics", [])
    current_level = tool_context.state.get("current_level", difficulty)

    with open("difficulty_guide.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter available topics
    candidates = [
        item for item in data
        if item.get("difficulty") == difficulty
        and item.get("question") not in used_topics
    ]

    if not candidates:
        return None

    selected = random.choice(candidates)

    # Persist topic usage in session state
    used_topics.append(selected["question"])
    tool_context.state['used_topics'] = used_topics
    tool_context.state['current_level'] = difficulty

    return {
        "difficulty": difficulty,
        "question": selected.get("question"),
        "answer": selected.get("answer")
    }

