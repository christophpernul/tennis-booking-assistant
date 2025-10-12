#!/usr/bin/env python3
"""
CLI script to run the Tennis Booking Assistant.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

import chainlit as cl


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

load_environment()

if not check_requirements():
    sys.exit(1)

# Get OpenAI API key and model name
openai_api_key = os.getenv(ENV_VAR_NAME_OPENAI_API_KEY)
openai_model = os.getenv(ENV_VAR_NAME_MODEL_NAME, "gpt-4o-mini")
# Get port from environment variable
port = int(os.environ.get(ENV_VAR_NAME_SERVER_PORT, 8000))
# Get server name (0.0.0.0 for Cloud Run, 127.0.0.1 for local)
server_name = os.environ.get(ENV_VAR_NAME_SERVER_NAME, "127.0.0.1")

print("✅ Tennis Booking Assistant is ready!")
print("🌐 Opening web interface...")

agent = BookingManager(openai_api_key, openai_model)


@cl.on_chat_start
async def on_chat_start():
    # TODO: Starters not working!
    # starters = [
    #     cl.Starter(
    #         label="Heute 18 Uhr",
    #         message="Gibt es heute um 18 Uhr verfügbare Plätze?",
    #         icon="/public/write.svg",
    #     ),
    #     cl.Starter(
    #         label="Freie Hallenplätze am Abend",
    #         message="Gibt es in den nächsten drei Tagen freie Plätze in der Halle ab 18 Uhr?",
    #         icon="/public/write.svg",
    #     ),
    # ]
    # cl.user_session.set("starters", starters)
    await cl.Message(content="Willkommen zum Tennis Buchungsassistenten!").send()


@cl.on_message
async def on_message(message: cl.Message):
    user_message = message.content
    response, _ = await agent.run(user_message)
    await cl.Message(content=response).send()
