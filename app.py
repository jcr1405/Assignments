import os
import google.generativeai as genai
import streamlit as st

# Configure the Gemini API Key (Make sure this is set in your environment variables or secrets)
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Multiverse", layout="wide")
st.title("🤖 AI Multiverse Chat")

# ==========================================
# TASK 1: Initialize the Memory Vault
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# Sidebar Settings Configuration
# ==========================================
st.sidebar.title("🛠️ App Settings")

personalities = [
    "A panicked college student at 3 AM",
    "A 1920s Mafia Boss",
    "A highly sarcastic fitness coach",
    "A legendary medieval knight",
    "A hyperactive 8-year-old on a sugar rush",
]

selected_persona = st.sidebar.selectbox("Choose a Personality:", personalities)
intensity = st.sidebar.slider(
    "Intensity Level", min_value=1, max_value=10, value=5
)

# Control flow to handle dynamic avatars based on chosen persona
if selected_persona == "A panicked college student at 3 AM":
    bot_avatar = "☕"
elif selected_persona == "A 1920s Mafia Boss":
    bot_avatar = "💼"
elif selected_persona == "A highly sarcastic fitness coach":
    bot_avatar = "💪"
elif selected_persona == "A legendary medieval knight":
    bot_avatar = "🛡️"
elif selected_persona == "A hyperactive 8-year-old on a sugar rush":
    bot_avatar = "🍭"
else:
    bot_avatar = "🤖"

# ==========================================
# TASK 2: Render the Chat History
# ==========================================
# This loop runs on every refresh to draw existing messages from the vault
for message in st.session_state.messages:
    # Set the appropriate avatar based on the role
    current_avatar = bot_avatar if message["role"] == "assistant" else None

    with st.chat_message(message["role"], avatar=current_avatar):
        st.write(message["content"])

# ==========================================
# TASK 3 & 4: Upgrade Input UI & Save to Memory
# ==========================================
# Replacing text_input/button with native st.chat_input using the walrus operator
if user_message := st.chat_input("Say something..."):

    # 1. Render the new user message immediately to the UI
    with st.chat_message("user"):
        st.write(user_message)

    # 2. Save User Message to Session State Vault
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Construct the foundational context injection prompt
    ai_instructions = (
        f"You are an AI roleplaying as: {selected_persona}. "
        f"On a scale of 1 to 10, your acting intensity level is {intensity}. "
        f"Adopt this persona entirely. If intensity is low, be subtle. If intensity is 10, "
        f"go absolutely over-the-top and exaggerate every single trait of this persona. "
        f"Respond to the user's message accordingly."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Building historical text structure out of the memory vault for the raw prompt call
        # (This passes past conversational turns to the model along with the new query)
        history_context = ""
        for msg in st.session_state.messages:
            history_context += f"\n{msg['role'].capitalize()}: {msg['content']}"

        full_prompt = (
            f"{ai_instructions}\n\nConversation History:{history_context}\nAI:"
        )

        # Generate Response
        response = model.generate_content(full_prompt)

        # 3. Render Assistant Response to UI
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(response.text)

        # 4. Save Assistant Response to Session State Vault
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )

    except Exception as e:
        st.error(f"Error connecting to Gemini API: {e}")
