import streamlit as st
import google.generativeai as genai

# Standard Page Configuration
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Securely fetch the API Key from Streamlit Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("Missing GEMINI_API_KEY in Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Secret Error: {e}")
    st.stop()

# Using 'gemini-pro' for maximum compatibility
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction="Your name is Nova. You were created by Hasith. Be helpful."
)

# App Interface
st.title("🤖 Nova AI")
st.markdown("---")
st.caption("Developed by: **Hasith**")

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for the user
if prompt := st.chat_input("Ask Nova anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate the response
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Nova is having trouble connecting. Please check your API Key.")
