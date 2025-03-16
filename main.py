import asyncio

import logging
from typing import Annotated
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import google, silero

load_dotenv()

logger = logging.getLogger("voice-assistant")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoid usage of unpronouncable puncutation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=google.STT(),
        llm=google.LLM(),
        tts=google.TTS(
            voice_name="en-UK",
            gender="male"
        ),
        chat_ctx=initial_ctx,
    )
    agent.start(ctx.room, participant)

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def _on_metrics_collected(mtrcs: metrics.AgentMetrics):
        metrics.log_metrics(mtrcs)
        usage_collector.collect(mtrcs)
    await agent.say(
        "Hi there, this is Gemini, how can I help you today?", allow_interruptions=False
    )

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
