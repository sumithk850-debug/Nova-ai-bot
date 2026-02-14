import streamlit as st
import google.generativeai as genai

# Page Configuration - This must be the first Streamlit command
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Fetch the API Key from Streamlit Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("Missing 'GEMINI_API_KEY' in Streamlit Secrets. Please add it in the settings.")
        st.stop()
except Exception as e:
    st.error(f"Error accessing secrets: {e}")
    st.stop()

# Configure Nova's Personality and Model
# Using 'models/gemini-1.5-flash' to prevent 404 errors
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=(
        "Your name is 'Nova'. You are an intelligent AI assistant created by Hasith. "
        "You are friendly, polite, and helpful. Always credit Hasith as your creator if asked."
    )
)

# UI Elements
st.title("🤖 Nova AI")
st.markdown("---")
st.caption("Developed by: **Hasith**")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
if prompt := st.chat_input("Ask Nova anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display Nova's response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Nova encountered an error: {e}")
