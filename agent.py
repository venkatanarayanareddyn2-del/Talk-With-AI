from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions

# plugin imports (import the concrete classes/modules)
from livekit.plugins.noise_cancellation import BVC
from livekit.plugins import google as google_beta

from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google_beta.beta.realtime.RealtimeModel(
                voice="Charon",
                temperature=0.8,
            ),
            tools=[get_weather, search_web],  # make sure these are valid callables/tools
        )


async def entrypoint(ctx: agents.JobContext):
    # ensure the job context is connected so ctx.room is available
    await ctx.connect()

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            audio_enabled=True,
            noise_cancellation=BVC(),  # instance of the noise cancellation plugin
        ),
    )

    await session.generate_reply(instructions=SESSION_INSTRUCTION)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
