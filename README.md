
# AI Daily Briefing Agent

An AI-powered daily briefing application that collects information from multiple external services and generates a concise, structured briefing for a user-provided topic.

The project demonstrates **Google Agent Development Kit (ADK)**, **Model Context Protocol (MCP)**, tool integration, Pydantic data validation, logging, testing, Streamlit, Docker containerization, GitHub Actions CI, and GitHub Container Registry.

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
- Support local Python execution
- Support Docker-based execution
- Publish Docker images to GitHub Container Registry
- Include unit tests and mocked API tests
- Maintain structured application logging
- Run automated CI through GitHub Actions

---

## Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         │   Enters a topic     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Streamlit UI      │
                         │       app.py         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Daily Briefing     │
                         │     ADK Agent        │
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

### Application Workflow

```text
User enters topic
       ↓
Streamlit sends request to ADK agent
       ↓
ADK agent invokes MCP tools
       ↓
News, weather, and finance data are retrieved
       ↓
Responses are validated using Pydantic models
       ↓
Gemini generates the daily briefing
       ↓
Structured briefing is displayed in Streamlit
```

---

## Technology Stack

- **Python 3.11**
- **Google Agent Development Kit**
- **Model Context Protocol**
- **MCP Toolset**
- **Google Gemini**
- **Pydantic**
- **Streamlit**
- **HTTPX**
- **Uvicorn**
- **Pytest**
- **Docker**
- **GitHub Actions**
- **GitHub Container Registry**
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
│   └── tools/
│       ├── __init__.py
│       ├── news_tool.py
│       ├── weather_tool.py
│       └── finance_tool.py
│
├── mcp_servers/
│   ├── __init__.py
│   └── briefing_mcp_server.py
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
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
└── README.md
```

> The actual `.env` file is intentionally excluded from GitHub because it contains secrets.

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

For detailed output:

```bash
pytest -v
```

The test suite includes:

- Unit tests for news, weather, and finance tools
- Pydantic model validation tests
- Mocked external API tests
- Error-handling tests
- Input validation tests

### Running Tests in CI Mode

The project supports running tests without a production API key:

```powershell
$env:APP_ENV="test"
pytest -v
```

GitHub Actions sets `APP_ENV=test` automatically.

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

### Docker Image and Container

```text
Dockerfile
    ↓ docker build
Docker Image
    ↓ docker run
Docker Container
    ↓
Running Streamlit Application
```

- **Dockerfile**: Build instructions
- **Docker image**: Packaged application
- **Docker container**: Running instance of the image

---

## Build the Docker Image Locally

From the project root, run:

```bash
docker build -t ai-daily-briefing-agent .
```

Explanation:

```text
docker build
    → Builds a Docker image

-t
    → Assigns a name and tag

ai-daily-briefing-agent
    → Image name

.
    → Uses the current directory as the build context
```

### Verify the Local Image

```bash
docker images
```

You should see an image similar to:

```text
REPOSITORY                  TAG       IMAGE ID       CREATED          SIZE
ai-daily-briefing-agent     latest    xxxxxxxxxxxx   A few seconds ago ...
```

---

## Run the Docker Container Locally

Run:

```bash
docker run --rm -p 8501:8501 --env-file .env ai-daily-briefing-agent
```

Explanation:

```text
docker run
    → Starts a container from the image

--rm
    → Removes the container after it stops

-p 8501:8501
    → Maps local port 8501 to container port 8501

--env-file .env
    → Loads environment variables from the local .env file

ai-daily-briefing-agent
    → Image to run
```

Open the application:

```text
http://localhost:8501
```

### Run on a Different Local Port

If port `8501` is already in use:

```bash
docker run --rm -p 8502:8501 --env-file .env ai-daily-briefing-agent
```

Then open:

```text
http://localhost:8502
```

### Stop the Container

Press:

```text
Ctrl + C
```

The `--rm` option automatically removes the stopped container. The Docker image remains available locally.

---

## GitHub Actions CI Pipeline

The project uses GitHub Actions to automatically:

1. Check out the source code
2. Set up Python
3. Install dependencies
4. Run tests
5. Build the Docker image
6. Publish the Docker image to GitHub Container Registry

### CI Workflow

```text
GitHub push
    ↓
GitHub Actions triggered
    ↓
Checkout source code
    ↓
Install Python dependencies
    ↓
Run pytest
    ↓
Build Docker image
    ↓
Login to GHCR
    ↓
Push Docker image to GHCR
```

The workflow file is located at:

```text
.github/workflows/ci.yml
```

---

## GitHub Container Registry

The Docker image is published to **GitHub Container Registry (GHCR)**.

### Published Image

```text
ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

A commit-specific image tag is also published for traceability:

```text
ghcr.io/sravyaspandana/ai-daily-briefing-agent:<commit-sha>
```

The `latest` tag points to the most recently published image.

The commit SHA tag identifies the exact source-code version used to build that image.

---

## Pull the Image from GHCR

Because the package is public, you can pull it without logging in:

```bash
docker pull ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

Verify that the image was downloaded:

```bash
docker images
```

You should see:

```text
ghcr.io/sravyaspandana/ai-daily-briefing-agent
```

---

## Run the GHCR Image Locally

Run the image pulled from GitHub Container Registry:

```bash
docker run --rm -p 8501:8501 --env-file .env ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

Open the application:

```text
http://localhost:8501
```

This verifies that the application can run from the **published registry image**, rather than only from a locally built image.

---

## GHCR Image Commands Summary

### Pull the latest image

```bash
docker pull ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

### Run the latest image

```bash
docker run --rm -p 8501:8501 --env-file .env ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

### List local images

```bash
docker images
```

### List running containers

```bash
docker ps
```

### List all containers

```bash
docker ps -a
```

### Stop a container

```bash
docker stop <container-id>
```

### Remove a local image

```bash
docker rmi ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

---

## GHCR Publishing Authentication

GitHub Actions uses the built-in `GITHUB_TOKEN` to authenticate with GHCR.

The workflow includes:

```yaml
permissions:
  contents: read
  packages: write
```

The login step is:

```yaml
- name: Log in to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

The image is built and pushed using:

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: |
      ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
      ghcr.io/sravyaspandana/ai-daily-briefing-agent:${{ github.sha }}
```

No personal access token is required for this workflow because GitHub provides the repository’s `GITHUB_TOKEN`.

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
- Invalid user input

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
- API keys are passed at runtime during container execution
- GitHub Actions tests do not require the production API key
- GHCR publishing uses GitHub’s built-in token

---

## Current Version

**Version: 1.0.0**

The project currently supports:

- Streamlit-based user interface
- Google ADK agent
- MCP tool integration
- News, weather, and finance tools
- Pydantic response validation
- Service health checks
- Structured logging
- Docker containerization
- GitHub Actions CI pipeline
- Docker image publishing to GHCR

---

## Future Enhancements

Potential future improvements include:

- Deploy the Docker image to AWS ECS
- Push the image to Amazon ECR
- Add ECS Fargate deployment
- Add Application Load Balancer
- Add automated release tagging
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
git commit -m "Update README with GHCR documentation"
```

Push changes to GitHub:

```bash
git push
```

---

## GitHub Repository

Repository:

https://github.com/SravyaSpandana/ai-daily-briefing-agent

## GitHub Container Registry

Published image:

```text
ghcr.io/sravyaspandana/ai-daily-briefing-agent:latest
```

---

## Author

**Sravya V**

Software Engineer | Java Full Stack | Cloud | Agentic AI