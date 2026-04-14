#!/bin/bash

set -a
source .env
set +a

uv run uvicorn server.remote_agent:a2a_app --host localhost --port 8001
