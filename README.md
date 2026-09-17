
# AI Daily Briefing Agent

An AI-powered daily briefing application that collects information from multiple external services and generates a concise, structured briefing for a user-provided topic.

The project demonstrates **Google Agent Development Kit (ADK)**, **Model Context Protocol (MCP)**, tool integration, Pydantic data validation, logging, testing, Streamlit, and Docker containerization.

---

## Features

- Generate a daily briefing for a user-provided topic
- Retrieve latest news articles
- Retrieve current weather information
- Retrieve financial information
- Use MCP tools through Google ADK
- Validate tool responses using Pydantic models
- Display the briefing through a Streamlit UI
- Perform external service health checks
- Support local execution and Docker-based execution
- Include unit tests and mocked API tests
- Maintain structured application logging

---

## Architecture

```text
                         ┌──────────────────────┐
                         │      User            │
                         │  Enters a topic      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Streamlit UI       │
                         │      app.py          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Daily Briefing      │
                         │  ADK Root Agent      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     MCP Toolset      │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │  News Service  │ │ Weather Service│ │ Finance Service│
        │ Google News RSS│ │   wttr.in      │ │ Yahoo Finance  │
        └────────────────┘ └────────────────┘ └────────────────┘
```

---

## Technology Stack

- **Python 3.11**
- **Google Agent Development Kit**
- **Model Context Protocol**
- **MCP Toolset**
- **Pydantic**
- **Streamlit**
- **HTTPX**
- **Uvicorn**
- **Google Gemini**
- **Pytest**
- **Docker**
- **Git and GitHub**

---

## Project Structure

```text
AIDailyBriefingAgent/
│
├── briefing_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── health_check.py
│   ├── logging_config.py
│   ├── models.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── news_tool.py
│   │   ├── weather_tool.py
│   │   └── finance_tool.py
│   │
│   └── ...
│
├── mcp_servers/
│   ├── __init__.py
│   ├── briefing_mcp_server.py
│   └── ...
│
├── tests/
│   ├── test_news_tool.py
│   ├── test_weather_tool.py
│   ├── test_finance_tool.py
│   ├── test_models.py
│   └── ...
│
├── docs/
│   └── architecture.md
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
├── README.md
└── .env
```

> The `.env` file contains local secrets and must not be committed to GitHub.

---

## Prerequisites

Install the following before running the project locally:

- Python 3.11 or later
- Git
- Visual Studio Code or another IDE
- Google Gemini API key
- Docker Desktop, if using Docker

---

## Environment Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

You can create a `.env.example` file for reference:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Never commit the actual `.env` file to GitHub.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/SravyaSpandana/ai-daily-briefing-agent.git
```

Move into the project directory:

```bash
cd ai-daily-briefing-agent
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## Running the Application Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

Enter a topic and generate the daily briefing.

---

## Running the MCP Server

The MCP server can be started using:

```bash
python -m mcp_servers.briefing_mcp_server
```

The server exposes tools used by the ADK agent, including:

- News retrieval
- Weather retrieval
- Finance retrieval

The ADK agent connects to the MCP server through the MCP toolset.

---

## Running Tests

Run all tests using:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

The test suite includes:

- Unit tests for news, weather, and finance tools
- Pydantic model validation tests
- Mocked external API tests
- Error-handling tests

---

## Service Health Checks

The application includes health checks for the external services used by the agent.

The health checks verify the availability of:

- News service
- Weather service
- Finance service

You can test the health-check module directly:

```bash
python -c "from briefing_agent.health_check import get_service_health; print(get_service_health())"
```

The Streamlit application also provides a **Service Health** option to check the external services.

---

## Docker Setup

Docker packages the Python runtime, project dependencies, application code, and MCP server into a portable image.

This allows the application to run consistently across different environments.

### Dockerfile

The project contains a `Dockerfile` in the root directory.

The Docker image includes:

- Python 3.11
- Required Python dependencies
- Application source code
- MCP server code
- Streamlit startup configuration

### Build the Docker image

From the project root, run:

```bash
docker build -t ai-daily-briefing-agent .
```

Explanation:

```text
docker build       → Builds a Docker image
-t                 → Assigns a name/tag to the image
ai-daily-briefing-agent → Image name
.                  → Uses the current directory as the build context
```

### Verify the image

```bash
docker images
```

You should see:

```text
ai-daily-briefing-agent
```

### Run the Docker container

```bash
docker run --rm -p 8501:8501 --env-file .env ai-daily-briefing-agent
```

Explanation:

```text
docker run       → Starts a container from the image
--rm             → Removes the container after it stops
-p 8501:8501     → Maps local port 8501 to container port 8501
--env-file .env  → Loads environment variables from the local .env file
ai-daily-briefing-agent → Image to run
```

Open the application:

```text
http://localhost:8501
```

### Run on a different local port

If port `8501` is already in use:

```bash
docker run --rm -p 8502:8501 --env-file .env ai-daily-briefing-agent
```

Then open:

```text
http://localhost:8502
```

### Stop the container

Press:

```text
Ctrl + C
```

The `--rm` option automatically removes the stopped container. The Docker image remains available.

---

## Docker Image and Container Concept

```text
Dockerfile
    ↓ docker build
Docker Image
    ↓ docker run
Docker Container
    ↓
Running Streamlit Application
```

The Dockerfile is the build recipe.

The Docker image is the packaged application.

The Docker container is the running instance of that image.

---

## External Services

The application uses external services to retrieve information:

| Service | Purpose |
|---|---|
| Google News RSS | News articles |
| wttr.in | Weather information |
| Yahoo Finance chart API | Financial information |
| Google Gemini | AI-generated briefing |

External service availability, rate limits, and response formats may change.

---

## Error Handling

The application includes handling for common external-service issues, such as:

- Request failures
- Timeout errors
- Invalid responses
- Missing data
- Service unavailability
- API quota errors

The application also uses logging to help troubleshoot failures.

---

## Logging

Logging is configured through:

```text
briefing_agent/logging_config.py
```

Logs help track:

- Tool execution
- External API calls
- Agent workflow activity
- Errors and exceptions
- Service health-check results

---

## Security Considerations

- API keys are loaded through environment variables
- `.env` is excluded from Git
- Secrets are not hardcoded in source code
- Docker builds do not include the local `.env` file
- API keys should be passed at runtime during container execution

---

## Future Enhancements

Potential future improvements include:

- Deploy the Docker image to AWS ECS
- Push the image to Amazon ECR
- Add GitHub Actions CI/CD
- Add automated Docker image builds
- Add richer Streamlit visualizations
- Add persistent storage
- Add authentication
- Add more MCP tools
- Add additional news and financial data sources
- Add monitoring with CloudWatch, Prometheus, or Grafana
- Add deployment through Spinnaker
- Support multi-agent workflows for more briefing categories

---

## Git Workflow

Check the current Git status:

```bash
git status
```

Stage changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Add Docker support and documentation"
```

Push changes to GitHub:

```bash
git push
```

---

## GitHub Repository

Repository:

https://github.com/SravyaSpandana/ai-daily-briefing-agent

---

## Author

**Sravya V**

Software Engineer | Java Full Stack | Cloud | Agentic AI