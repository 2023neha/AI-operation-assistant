# AI-operation-assistant
AI operation assistant



A multi-agent AI system built with Python and Streamlit that can plan, execute, and verify tasks using integrated tools like Weather and Crypto APIs.

##  Architecture

The system uses an **Orchestrator-Worker** multi-agent architecture:

1.  **Orchestrator**: Manages the lifecycle of a user request.
2.  **Planner Agent**: Breaks down the user request into a step-by-step logical plan.
3.  **Executor Agent**: Executes each step of the plan by calling the appropriate tools.
4.  **Verifier Agent**: Review the tool outputs and execution logs to ensure the original user request was satisfied.

**Integrated Tools:**
*   **Weather Tool**: Fetches current weather data via OpenMeteo API.
*   **Crypto Tool**: Fetches cryptocurrency prices via CoinGecko API.

##  Setup Instructions

### Prerequisites
*   Python 3.8+
*   A Google Gemini API Key (Get it from [AI Studio](https://aistudio.google.com/))

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Copy the example environment file and add your API key.
    ```bash
    cp .env.example .env
    ```
    Open `.env` and paste your `GEMINI_API_KEY`.

### Running Locally

Run the Streamlit application:
```bash
streamlit run app.py
```
Access the web interface at `http://localhost:8501`.

## 🔑 Environment Variables

See `.env.example` for reference.

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API Key | Yes |
| `OPENAI_BASE_URL` | Base URL for LLM client (defaults to Google's endpoint) | No |

# Integrated APIs

*   **Google Gemini API**: For reasoning, planning, and natural language generation.
*   **OpenMeteo API**: Free weather API (no key required).
*   **CoinGecko API**: Cryptocurrency data API (free tier used).

##  Example Prompts

Try these prompts in the application:

1.  *"What is the current price of Bitcoin?"*
2.  *"Get the weather in Tokyo and the price of Ethereum."*
3.  *"Check the temperature in London."*
4.  *"What is the price of Solana?"*
5.  *"Find the weather in New York and Paris."*

##  Known Limitations & Tradeoffs

*   **Tool Limitation**: Currently only supports Weather and Crypto data. It cannot access Gmail, Calendar, or other external services yet.
*   **Statelessness**: The agents treat each request as a new task; complex multi-turn context (memory of previous tool calls across different sessions) is limited.
*   **Rate Limits**: The CoinGecko free API has rate limits which might cause errors if queried too frequently.
*   **LLM Dependency**: Heavily relies on the reasoning capability of the underlying LLM (Gemini) for accurate planning.
