import streamlit as st

# Task 1: The UI Shell
st.title("The Identity Echo Interface")
st.write("Enter your identity and message below, then transmit your message.")

# Task 2: Multi-Data Collection
user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")

# Task 3: The Action Gate
if st.button("Transmit"):

    # Task 4: Conditional Routing (Edge Cases)
    if not user_name:
        st.error("Please provide your name.")

    elif not user_message:
        st.warning("Please type a message to transmit.")

    # Task 5: The Formatted Output
    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. "
            f"We received your message: {user_message}"
        )

        # Advanced Challenge: Token Cost Estimator
        character_count = len(user_message)
        token_count = character_count / 4

        st.info(
            f"System Check: Your message will consume approximately "
            f"{token_count:.2f} tokens from our context window."
        )
