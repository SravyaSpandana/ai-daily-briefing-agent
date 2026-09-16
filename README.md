# AI Daily Briefing Agent

An agentic AI application that generates concise daily briefings using Google Agent Development Kit, Gemini, MCP tools, and Streamlit.

The application can retrieve current news, weather information, and recent financial market data, then use Gemini to organize the results into a structured briefing.

---

## Overview

The AI Daily Briefing Agent is designed to demonstrate how an LLM can be combined with external tools and MCP to build a practical agentic AI application.

Instead of relying only on the model's existing knowledge, the agent can invoke external tools to retrieve current information and then summarize the results.

### Main capabilities

- Retrieve current news for a topic
- Retrieve current weather for a location
- Retrieve recent market information for a stock symbol
- Use Google ADK to orchestrate the agent workflow
- Use Gemini as the reasoning and summarization model
- Expose tools through an MCP server
- Connect MCP tools to the ADK agent
- Display results through a Streamlit web interface
- Handle unavailable data and service errors
- Generate structured Markdown briefings

---

## Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Google ADK Runner │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Daily Briefing Agent│
                         │   Gemini LLM        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     MCPToolset      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │     Briefing MCP Server      │
                    └──────────────┬───────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             ▼                     ▼                     ▼
      ┌────────────┐       ┌────────────┐       ┌────────────┐
      │ News Tool  │       │Weather Tool│       │Finance Tool│
      └─────┬──────┘       └─────┬──────┘       └─────┬──────┘
            │                    │                    │
            ▼                    ▼                    ▼
       News RSS             Weather API          Market API
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 ▼
                         Tool results returned
                                 │
                                 ▼
                         Gemini summarizes
                                 │
                                 ▼
                         Final daily briefing
```

---

## Technology Stack

- Python
- Google Agent Development Kit
- Gemini
- MCP
- MCP 2.x
- Pydantic
- Streamlit
- HTTPX
- python-dotenv
- Google News RSS
- wttr.in weather service
- Yahoo Finance chart endpoint

---

## Project Structure

```text
AIDailyBriefingAgent/
│
├── briefing_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── news_tool.py
│   ├── weather_tool.py
│   └── finance_tool.py
│
├── mcp_servers/
│   ├── __init__.py
│   └── briefing_mcp_server.py
│
├── data/
├── tests/
│
├── app.py
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Component Description

### `briefing_agent/agent.py`

Defines the root Google ADK agent.

Responsibilities:

- Configure the Gemini model
- Define the agent instructions
- Connect the MCP toolset
- Decide when tools should be called
- Summarize tool results
- Generate the final briefing

### `briefing_agent/config.py`

Loads environment variables from the `.env` file.

### `briefing_agent/news_tool.py`

Retrieves recent news headlines using Google News RSS.

The tool returns:

- Headline
- Source
- Publication date
- Article link

### `briefing_agent/weather_tool.py`

Retrieves current weather information using wttr.in.

The tool returns:

- Weather condition
- Temperature
- Feels-like temperature
- Humidity
- Wind speed

### `briefing_agent/finance_tool.py`

Retrieves recent market information using a Yahoo Finance chart endpoint.

The tool returns:

- Latest closing price
- Change from previous close
- Opening price
- Day high
- Day low
- Trading volume

### `mcp_servers/briefing_mcp_server.py`

Exposes the News, Weather, and Finance functions as MCP tools.

Available MCP tools:

```text
news(topic)
weather(location)
finance(symbol)
```

### `app.py`

Provides the Streamlit user interface.

The UI allows the user to enter:

- News topic
- Weather location
- Stock symbol

It then invokes the ADK agent and displays the generated briefing.

---

## Agent Workflow

```text
User enters a request
        ↓
Streamlit creates a prompt
        ↓
ADK Runner invokes the root agent
        ↓
Gemini interprets the request
        ↓
Gemini selects the required MCP tools
        ↓
MCPToolset communicates with the MCP server
        ↓
MCP server invokes the corresponding Python functions
        ↓
External services return data
        ↓
Tool results are passed back to Gemini
        ↓
Gemini summarizes and structures the results
        ↓
Streamlit displays the final briefing
```

---

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/SravyaSpandana/ai-daily-briefing-agent.git
```

Move into the project directory:

```powershell
cd ai-daily-briefing-agent
```

---

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
```

```powershell
pip install -r requirements.txt
```

---

### 4. Configure the Google API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

The `.env` file is ignored by Git and must never be committed to GitHub.

The `.env.example` file contains only a placeholder:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## Requirements

The current dependencies are:

```text
google-adk
mcp
pydantic
python-dotenv
streamlit
httpx
```

The project currently uses:

```text
Google ADK 2.9.1
MCP 2.2.0
```

---

## Running the Application

### Run the Streamlit application

From the project root:

```powershell
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

The Streamlit interface allows you to enter:

- A news topic, such as `artificial intelligence`
- A weather location, such as `Hyderabad`
- A stock symbol, such as `JPM`

Click **Generate Briefing** to invoke the agent.

---

### Run ADK Web

To test the agent through the Google ADK development interface:

```powershell
adk web
```

Open the URL displayed in the terminal.

Use prompts such as:

```text
Give me current news about artificial intelligence.
```

```text
What is the current weather in Hyderabad?
```

```text
Give me a recent market snapshot for JPM.
```

```text
Prepare a daily briefing with AI news, Hyderabad weather, and JPM market information.
```

---

### Run the MCP server manually

The MCP server can be started manually with:

```powershell
python -m mcp_servers.briefing_mcp_server
```

The server uses standard input/output transport and waits for an MCP client.

Normally, the server is started automatically by the ADK `MCPToolset`, so manual execution is not required when running the Streamlit application or ADK Web.

---

## Example Prompt

```text
Prepare my daily briefing.

Include:
- Current artificial intelligence news
- Current weather in Hyderabad
- Recent market information for JPM

Keep it concise and use the structured format.
```

---

## Expected Response Format

```markdown
## Daily Briefing

### News Highlights

- Important current news headline
- Source and article link

### Weather

- Location: Hyderabad
- Condition: ...
- Temperature: ...
- Feels like: ...
- Humidity: ...
- Wind speed: ...

### Market Snapshot

- Symbol: JPM
- Latest close: ...
- Change from previous close: ...
- Open: ...
- Day high: ...
- Day low: ...
- Volume: ...

This information is not financial advice.

### Important Notes

- Any unavailable data or service limitations

### Sources

- Source links returned by the tools
```

---

## MCP Integration

The project uses MCP to expose external capabilities in a standardized way.

The MCP server defines three tools:

```python
news(topic: str)
weather(location: str)
finance(symbol: str)
```

The Google ADK agent connects to the MCP server using `MCPToolset`.

Conceptually:

```text
ADK Agent
    ↓
MCPToolset
    ↓
MCP Server
    ↓
MCP Tool
    ↓
External Data Service
```

This approach separates:

- Agent reasoning
- Tool implementation
- MCP communication
- User interface

---

## Error Handling

The tools handle common failures, including:

- Missing input
- HTTP request failures
- Invalid service responses
- Missing data
- Unexpected exceptions

The agent is instructed to:

- Avoid inventing current information
- Clearly mention unavailable data
- Distinguish retrieved information from general knowledge
- Avoid presenting market information as financial advice

---

## Current Status

- [x] Project initialized
- [x] Python virtual environment configured
- [x] Dependencies installed
- [x] Environment configuration added
- [x] Gemini-based ADK root agent created
- [x] News tool added
- [x] Weather tool added
- [x] Finance tool added
- [x] MCP server created
- [x] MCP 2.x compatibility updated
- [x] MCP server connected to Google ADK
- [x] News tool tested through ADK
- [x] Weather tool tested through ADK
- [x] Finance tool tested through ADK
- [x] Streamlit UI created
- [x] End-to-end briefing tested
- [x] Structured Markdown response format added

---

## Future Enhancements

- Strict structured output using Pydantic models
- Separate specialized News, Weather, and Finance agents
- Agent-to-agent communication using A2A
- Briefing history and persistence
- User preferences and personalized briefings
- Scheduled daily briefing generation
- Email or notification delivery
- RAG over saved news articles
- Improved source extraction and citations
- Better finance data provider integration
- Unit and integration tests
- Docker support
- Cloud deployment
- Authentication and multi-user support

---

## Security Notes

- Never commit the `.env` file.
- Never expose the Google API key in source code.
- Do not upload API keys, credentials, or tokens to GitHub.
- Use `.env.example` to document required environment variables.
- Treat external data as untrusted input.
- Do not treat market data as financial advice.

---

## License

This project is intended for learning, experimentation, and portfolio development.