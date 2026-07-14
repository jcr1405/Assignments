import os
import google.generativeai as genai
import streamlit as st

# Configure the Gemini API Key (Make sure this is set in your environment variables or secrets)
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Multiverse", layout="wide")
st.title("🤖 AI Multiverse Chat")

# ==========================================
# TASK 1: UI Cleanup & TASK 3: Slider
# ==========================================
st.sidebar.title("🛠️ App Settings")

# TASK 2: Persona Expansion
personalities = [
    "A panicked college student at 3 AM",
    "A 1920s Mafia Boss",
    "A highly sarcastic fitness coach",
    "A legendary medieval knight",
    "A hyperactive 8-year-old on a sugar rush",
]

selected_persona = st.sidebar.selectbox("Choose a Personality:", personalities)

# TASK 3: Parameter Tuning (The Slider)
intensity = st.sidebar.slider(
    "Intensity Level", min_value=1, max_value=10, value=5
)

# ==========================================
# TASK 5: Dynamic Avatars (Control Flow)
# ==========================================
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
# Main Chat UI & Logic
# ==========================================

# User Input Field
user_message = st.text_input("Type your message here...", key="chat_input")
send_button = st.button("SEND")

# TASK 4: Visual Upgrade (Chat Elements) & API Call
if send_button and user_message:
    # Render the user's message in a chat bubble
    with st.chat_message("user"):
        st.write(user_message)

    # TASK 3: Prompt Engineering Update with f-string injecting personality and intensity
    ai_instructions = (
        f"You are an AI roleplaying as: {selected_persona}. "
        f"On a scale of 1 to 10, your acting intensity level is {intensity}. "
        f"Adopt this persona entirely. If intensity is low, be subtle. If intensity is 10, "
        f"go absolutely over-the-top and exaggerate every single trait of this persona. "
        f"Respond to the user's message accordingly."
    )

    try:
        # Initialize the model and generate the content
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Combining instructions and user query for the model
        full_prompt = f"{ai_instructions}\n\nUser: {user_message}\nAI:"
        response = model.generate_content(full_prompt)

        # Render the AI's response using the native chat bubble and dynamic avatar
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(response.text)

    except Exception as e:
        st.error(f"Error connecting to Gemini API: {e}")
