#!/usr/bin/env python3
"""
CLI script to run the Tennis Booking Assistant.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

import chainlit as cl
from chainlit.user import User


def load_environment():
    """Load environment variables from .env file."""
    # Look for .env file in project root
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    if env_file.exists():
        load_dotenv(env_file, override=True)
    else:
        # Try to load from current directory
        load_dotenv(override=True)


# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.constants import (
    ENV_VAR_NAME_SERVER_NAME,
    ENV_VAR_NAME_SERVER_PORT,
    ENV_VAR_NAME_MODEL_NAME,
    ENV_VAR_NAME_OPENAI_API_KEY,
)
from src.utils.validation import check_requirements
from src.agent.openai_agent.agent import BookingManager

WELCOME_TEXT: str = (
    "**Willkommen zum Tennis Buchungsassistenten!**\n\n"
    "Frage nach freien Plätzen im STC München...\n\n"
    "_Beispiele_\n"
    "Ich möchte heute um 18 Uhr am T-Platz spielen.\n"
    "Ich suche freie Hallenplätze für morgen Abend ab 19 Uhr."
)

############################### START CODE ##########################################

load_environment()

if not check_requirements():
    sys.exit(1)

# Get OpenAI API key and model name
OPENAI_API_KEY = os.getenv(ENV_VAR_NAME_OPENAI_API_KEY)
LLM_MODEL_NAME = os.getenv(ENV_VAR_NAME_MODEL_NAME, "gpt-4o-mini")
# Get port from environment variable
SERVER_PORT = int(os.environ.get(ENV_VAR_NAME_SERVER_PORT, 8000))
# Get server name (0.0.0.0 for Cloud Run, 127.0.0.1 for local)
SERVER_NAME = os.environ.get(ENV_VAR_NAME_SERVER_NAME, "127.0.0.1")

OAUTH_GOOGLE_CLIENT_ID = os.environ.get("OAUTH_GOOGLE_CLIENT_ID")
OAUTH_GOOGLE_CLIENT_SECRET = os.environ.get("OAUTH_GOOGLE_CLIENT_SECRET")


@cl.oauth_callback
async def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: dict,
    default_user: User,
) -> User:
    """
    This function is called when the user successfully authenticates.
    Customize user data and metadata here.
    """
    print("OAuth callback called!")
    # You can add custom logic here to:
    # - Store user in your database
    # - Add custom metadata
    # - Implement role-based access control

    return default_user


@cl.on_chat_start
async def on_chat_start():
    agent = BookingManager(OPENAI_API_KEY, LLM_MODEL_NAME)
    cl.user_session.set("agent", agent)
    print("✅ Tennis Booking Assistant is ready!")

    user = cl.user_session.get("user")
    print(f"A new chat session has started for user {user.identifier}!")
    await cl.Message(content=WELCOME_TEXT).send()


@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")

    user_message = message.content
    response, _ = await agent.run(user_message)
    await cl.Message(content=response).send()
