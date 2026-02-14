import streamlit as st
import google.generativeai as genai

# Fetch the API Key from Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Please add the 'GEMINI_API_KEY' in Streamlit Secrets.")
    st.stop()

# Configure Nova's Personality and Creator Info
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Your name is 'Nova'. You were created by 'Hasith'. "
                       "You are a helpful and friendly AI assistant. "
                       "Always mention that Hasith created you if asked about your origin."
)

# Page Layout Configuration
st.set_page_config(page_title="Nova AI", page_icon="🤖")
st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

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
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")
