# app.py
import json
import os
import uuid
import asyncio
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Load .env file if available
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Set page config for a premium look
st.set_page_config(
    page_title="☕ Coffee Shop - Barista Bot",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sticky header
st.markdown("""
<style>
    div[data-testid="element-container"]:has(.header-container),
    div.element-container:has(.header-container) {
        position: sticky;
        top: 2.875rem;
        z-index: 999;
        background-color: transparent;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="header-container" style="text-align: center; padding: 20px; background: linear-gradient(135deg, #8B5E3C, #6F4E37); color: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700; color: white;">☕ Coffee Shop RAG Barista</h1>
    <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">Powered by Google ADK 2.x, Streamlit, and Gemini API</p>
</div>
""", unsafe_allow_html=True)

# Load Menu for the sidebar
menu_file = Path(__file__).parent / "menu.json"
try:
    with open(menu_file, "r") as f:
        menu_items = json.load(f)
except Exception as e:
    st.error(f"Error loading menu: {e}")
    menu_items = []

# Sidebar Menu & Configuration
with st.sidebar:
    st.markdown("## ☕ Coffee Shop Menu")
    st.markdown("Explore our offerings and ask the barista for recommendations.")
    st.markdown("---")

    for item in menu_items:
        with st.container(border=True):
            st.markdown(f"**{item['name']}**  •  **${item['price']:.2f}**")
            st.caption(item['description'])

            # Tags & Allergens as native badges
            tags = " ".join([f"`{t}`" for t in item.get("tags", [])])
            if tags:
                st.markdown(tags)

            allergens = ", ".join(item.get("allergens", []))
            if allergens:
                st.markdown(f"⚠️ *Allergens: {allergens}*")

# Chat Session State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "runner" not in st.session_state:
    from google.adk.runners import InMemoryRunner
    from agent import app
    st.session_state.runner = InMemoryRunner(app=app)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to ☕ Coffee Shop! What can I get started for you today?"}
    ]

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input & Interaction
if prompt := st.chat_input("Ask for recommendations (e.g., 'What dairy-free lattes or pastries do you have?')"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.chat_message("assistant"):
        try:
            async def fetch_response():
                return await st.session_state.runner.run_debug(
                    prompt,
                    session_id=st.session_state.session_id
                )

            res_events = asyncio.run(fetch_response())

            response_text = "".join([
                part.text
                for event in res_events
                if event.content and event.content.parts
                for part in event.content.parts
                if part.text
            ])

            if not response_text.strip():
                response_text = "I'm sorry, I couldn't generate a response. Please try asking again!"

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Apologies, I ran into an error: {e}")
