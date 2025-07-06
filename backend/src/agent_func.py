import logging
import os

import azure.functions as func
from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from src.agents.team_orchestrator import get_team

logging.getLogger().setLevel(logging.INFO)

model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    model=os.environ.get("AZURE_OPENAI_CHAT_MODEL"),
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
)

bp = func.Blueprint()


@bp.route(route="chats", methods=["POST"])
async def chat(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    task = req_body.get("task")

    # TODO: configure team and use it in the task
    team = get_team(model_client)

    stream = team.run_strean(task=task)
    async for chunk in stream:
        if isinstance(chunk, TaskResult):
            answer = chunk.messages[-1].content
        else:
            logging.info(f"-----{chunk.source} ({chunk.type} -----\n{chunk.content}")

        return func.HttpResponse(
            answer,
            status_code=200,
        )
