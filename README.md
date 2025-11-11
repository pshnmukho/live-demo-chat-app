# Streamlit + Gemini Chat App

A minimal chat interface built with Streamlit using Google Gemini models.

## Local run
1. Create and activate a virtual environment (optional).
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your API key in your shell:
   ```bash
   set GEMINI_API_KEY=YOUR_KEY   # Windows
   # export GEMINI_API_KEY=YOUR_KEY  # macOS/Linux
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy (Streamlit Community Cloud)
1. Push this folder to a public GitHub repo.
2. In Streamlit Cloud, create a new app from that repo.
3. In App settings → Secrets, add:
   ```
   GEMINI_API_KEY = your_key_here
   ```
4. Deploy.

## Notes
- Default model is `gemini-1.5-flash`. You can switch to `gemini-1.5-pro` in the sidebar.
- The app stores chat history in `st.session_state` during the session.
