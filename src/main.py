"""
Main entry point for the Tennis Booking Assistant application.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.interface.gradio_app import create_app


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


def check_requirements():
    """Check if required environment variables are set."""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file in the project root with:")
        for var in missing_vars:
            print(f"   {var}=your_value_here")
        return False
    
    return True


def main():
    """Main application entry point."""
    print("🎾 Starting Tennis Booking Assistant...")
    
    # Load environment variables
    load_environment()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Get OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Create and launch the Gradio app
    app = create_app(openai_api_key)
    
    print("✅ Tennis Booking Assistant is ready!")
    print("🌐 Opening web interface...")
    
    # Launch the app
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True if you want a public link
        show_error=True
    )


if __name__ == "__main__":
    main()

