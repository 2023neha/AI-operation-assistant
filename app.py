import streamlit as st
import os
from src.agents.orchestrator import Orchestrator

st.set_page_config(page_title="AI Operations Assistant", layout="wide")

def main():
    st.title("🤖 AI Operations Assistant")
    st.markdown("""
    This assistant plans, executes, and verifies tasks using a Multi-Agent Architecture.
    **Tools Available:** Weather (OpenMeteo), Crypto Price (CoinGecko).
    """)

    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Gemini API Key", type="password", help="Get it from https://aistudio.google.com/")
        base_url = st.text_input("Base URL (Optional)", value="https://generativelanguage.googleapis.com/v1beta/openai/")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
        if base_url:
            os.environ["OPENAI_BASE_URL"] = base_url

    if not os.getenv("GEMINI_API_KEY") and "GEMINI_API_KEY" not in os.environ:
         st.warning("⚠️ No Gemini API Key found! Please enter one in the sidebar or set it in a .env file.")


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your task (e.g., 'What is the price of Bitcoin and the weather in New York?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            st.write("🔄 **Starting Agent Workflow...**")
            
            orchestrator = Orchestrator()
            container = st.container()
            
            with container:
                for event in orchestrator.run(prompt):
                    event_type = event["type"]
                    
                    if event_type == "status":
                        st.info(event["content"])
                        
                    elif event_type == "plan":
                        st.write("📅 **Plan Created:**")
                        for i, step in enumerate(event["content"]):
                            st.write(f"{i+1}. {step}")
                            
                    elif event_type == "execution":
                        st.write(f"⚙️ **Executed:** {event['step']}")
                        st.code(event["result"])
                        
                    elif event_type == "verification":
                        st.write("✅ **Verification Result:**")
                        st.markdown(event["content"])
                        final_response = event["content"]
                        st.session_state.messages.append({"role": "assistant", "content": final_response})
                        
                    elif event_type == "error":
                        st.error(event["content"])

if __name__ == "__main__":
    main()
