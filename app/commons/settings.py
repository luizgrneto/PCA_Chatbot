"""Agent environment variables."""

import os
from typing import Dict

APP_NAME: str = os.environ.get("APP_NAME", "")
PROJECT: str = os.environ.get("PROJECT", "")
TEAM: str = os.environ.get("TEAM", "")
ARTIFACT_SERVICE_URI: str = os.environ.get("ARTIFACT_BUCKET_NAME", "")

AGENT_LABELS: Dict[str, str] = {
    "team": TEAM,
    "project": PROJECT,
    "agent_name": APP_NAME,
}
