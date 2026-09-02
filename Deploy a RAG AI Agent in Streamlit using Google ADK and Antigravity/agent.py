# agent.py
import json
import os
from pathlib import Path

# Load environment variables if .env file exists
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

from google.adk.agents import LlmAgent
from google.adk.apps import App

def get_menu() -> str:
    """Retrieves the coffee shop menu from menu.json.

    Returns:
        str: A JSON string representing the list of menu items with descriptions, prices, tags, and allergens.
    """
    menu_file = Path(__file__).parent / "menu.json"
    try:
        with open(menu_file, "r") as f:
            menu_data = json.load(f)
            return json.dumps(menu_data)
    except Exception as e:
        return json.dumps({"error": f"Could not retrieve menu: {str(e)}"})

# Configurable model name with gemini-3.6-flash default
MODEL_NAME = os.getenv("MODEL", "gemini-3.6-flash")

# Create the RAG Barista agent
barista_agent = LlmAgent(
    name="barista_agent",
    model=MODEL_NAME,
    instruction="""You are a friendly barista at ☕ Coffee Shop.
Your job is to recommend drinks and pastries to customers based on their preferences.

Rules you MUST follow:
1. You must recommend items ONLY from the menu returned by get_menu().
2. Do NOT recommend or suggest any item that is not present in the menu.
3. If a user's preference is vague or unclear, ask exactly ONE friendly clarifying question to narrow down what they want (e.g., cold or hot, sweet or strong, coffee or pastry).
4. Be warm and welcoming, but remain professional.
5. Ground your recommendations in the actual tags, descriptions, and allergens listed in the menu (e.g., if a user is dairy-free, recommend ONLY items tagged 'dairy-free' or with no dairy allergens).
""",
    tools=[get_menu]
)

# Define the ADK App object
app = App(
    name="coffee_barista_app",
    root_agent=barista_agent
)
