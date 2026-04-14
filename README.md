# ADK A2A Share State

A minimal example of sharing session state between ADK agents over the A2A protocol.

ADK's A2A communication is stateless by design — session state is not shared across process boundaries. This sample demonstrates a pattern to bridge that gap by forwarding client-side session state through A2A request metadata, making it available on the server side for instruction template resolution.

Blog: https://dev.to/koichi73/adk-passing-session-state-to-remote-agents-over-stateless-a2a-bfj

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Google Cloud project with Vertex AI API enabled
- Application Default Credentials configured (`gcloud auth application-default login`)

## Setup

```bash
cp .env.example .env
```

Fill in `.env`:

```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

Install dependencies:

```bash
uv sync
```

## Running

**Terminal 1 — start the A2A server:**

```bash
bash start_a2a_server.sh
```

The server starts at `http://localhost:8001`.

**Terminal 2 — run the client agent:**

```bash
uv run adk run client
# or use the web UI
uv run adk web
```

The root agent calls the remote `greet_agent` and receives a response like:

```
Hello Alice! How are you doing today?
```

## Project Structure

```
share_state/
├── client/
│   └── agent.py          # root_agent with RemoteA2aAgent + RequestInterceptor
├── server/
│   └── remote_agent.py   # greet_agent served via to_a2a()
├── start_a2a_server.sh
└── .env.example
```
