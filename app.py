import os
import streamlit as st

try:
    import google.generativeai as genai
except Exception as e:
    genai = None

st.set_page_config(page_title="Gemini Chat", page_icon="💬", layout="centered")

st.title("💬 Streamlit + Gemini Chat")
st.caption("Powered by Google Gemini 1.5 Flash")

# Retrieve API key: prefer environment variable, fallback to Streamlit secrets if available
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "GEMINI_API_KEY not found. Set it in Streamlit Cloud (App settings → Secrets) or as an environment variable on your machine.")
    st.stop()

if genai is None:
    st.error("Failed to import google-generativeai. Make sure dependencies are installed.")
    st.stop()

# Configure SDK
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Gemini client: {e}")
    st.stop()

MODEL_NAME = st.sidebar.selectbox(
    "Model",
    options=["gemini-1.5-flash", "gemini-1.5-pro"],
    index=0,
)

system_prompt = st.sidebar.text_area(
    "System prompt (optional)",
    value="You are a helpful AI assistant.",
    help="High-level behavior instructions for the assistant.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history for Gemini
    history = []
    if system_prompt:
        history.append({"role": "user", "parts": [f"System: {system_prompt}"]})
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [m["content"]]})

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        text = getattr(response, "text", None)
        if callable(text):
            text = response.text()
        if not text:
            # Some SDK versions expose .candidates[0].content.parts[0].text
            try:
                text = response.candidates[0].content.parts[0].text
            except Exception:
                text = "(No response text)"
    except Exception as e:
        text = f"Error from model: {e}"

    # Add assistant message to history and render
    st.session_state.messages.append({"role": "assistant", "content": text})
    with st.chat_message("assistant"):
        st.markdown(text)

# Sidebar tips
st.sidebar.markdown("---")
st.sidebar.markdown("**Tips**")
st.sidebar.markdown("- Set your `GEMINI_API_KEY` in Secrets for deployment.")
st.sidebar.markdown("- Switch between Flash and Pro as needed.")
