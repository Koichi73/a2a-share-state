from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext


def _inject_metadata_into_state(callback_context: CallbackContext) -> None:
    """Expand A2A metadata into the session state."""
    run_config = callback_context.run_config
    for key, value in (run_config.custom_metadata.get("a2a_metadata") or {}).items():
        callback_context.state[key] = value


greet_agent = Agent(
    model="gemini-3-flash-preview",
    name="greet_agent",
    description="Greet according to the format.",
    instruction="""
    Please greet according to the format.
    Hello {user_name}! How are you doing today? 
    """,
    before_agent_callback=_inject_metadata_into_state,
)


a2a_app = to_a2a(greet_agent, port=8001)
