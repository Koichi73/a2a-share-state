from typing import Any
from a2a.types import Message as A2AMessage
from google.adk.a2a.agent.config import (
    A2aRemoteAgentConfig,
    ParametersConfig,
    RequestInterceptor,
)
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.agent_tool import AgentTool

async def _forward_state_as_a2a_metadata(
    ctx: InvocationContext,
    a2a_request: A2AMessage,
    parameters: ParametersConfig,
) -> tuple[A2AMessage, ParametersConfig]:
    """before_request: Include all session state keys in the A2A metadata."""
    payload: dict[str, Any] = dict(ctx.session.state)
    if payload:
        parameters.request_metadata = {
            **(parameters.request_metadata or {}),
            **payload,
        }
    return a2a_request, parameters


greet_agent = RemoteA2aAgent(
    name="greet_agent",
    description="Greet according to the format.",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
    config=A2aRemoteAgentConfig(
        request_interceptors=[
            RequestInterceptor(before_request=_forward_state_as_a2a_metadata),
        ]
    ),
)


def _seed_state(callback_context: CallbackContext) -> None:
    """For demo purposes: set a fixed value to the state."""
    callback_context.state.setdefault("user_name", "Alice")


root_agent = Agent(
    name="root_agent",
    model="gemini-3-flash-preview",
    instruction="Please use the tool to greet the user.",
    tools=[AgentTool(greet_agent)],
    before_agent_callback=_seed_state,
)
