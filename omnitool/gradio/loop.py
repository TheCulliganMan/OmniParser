"""Agentic sampling loop that calls the Anthropic API and local implenmentation of anthropic-defined computer use tools."""

from collections.abc import Callable
from enum import StrEnum

from agent.anthropic_agent import AnthropicActor
from agent.vlm_agent import VLMAgent
from agent.vlm_agent_with_orchestrator import VLMOrchestratedAgent
from anthropic import APIResponse
from anthropic.types import (
    TextBlock,
)
from anthropic.types.beta import BetaContentBlock, BetaMessage, BetaMessageParam
from executor.anthropic_executor import AnthropicExecutor

from omnitool.gradio.agent.llm_utils.omniparserclient import OmniParserClient
from omnitool.gradio.tools import ToolResult
from omnitool.settings import (
    ModelChoice,
)

BETA_FLAG = "computer-use-2024-10-22"


class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    VERTEX = "vertex"
    OPENAI = "openai"
    AZURE_OPENAI = "azure-openai"


PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
    APIProvider.BEDROCK: "anthropic.claude-3-5-sonnet-20241022-v2:0",
    APIProvider.VERTEX: "claude-3-5-sonnet-v2@20241022",
    APIProvider.OPENAI: "gpt-4o",
    APIProvider.AZURE_OPENAI: "gpt-4o",
}


def sampling_loop_sync(
    *,
    model: str,
    provider: APIProvider | None,
    messages: list[BetaMessageParam],
    output_callback: Callable[[BetaContentBlock], None],
    tool_output_callback: Callable[[ToolResult, str], None],
    api_response_callback: Callable[[APIResponse[BetaMessage]], None],
    api_key: str,
    only_n_most_recent_images: int | None = 2,
    max_tokens: int = 4096,
    omniparser_url: str,
    save_folder: str = "./uploads",
):
    """Synchronous agentic sampling loop for the assistant/tool interaction of computer use."""
    print("in sampling_loop_sync, model:", model)
    omniparser_client = OmniParserClient(url=f"http://{omniparser_url}/parse/")
    if model == ModelChoice.CLAUDE_SONNET.value:
        # Register Actor and Executor
        actor = AnthropicActor(
            model=model,
            provider=provider,
            api_key=api_key,
            api_response_callback=api_response_callback,
            max_tokens=max_tokens,
            only_n_most_recent_images=only_n_most_recent_images,
        )
    elif model in set(
        [
            ModelChoice.OMNIPARSER_GPT4O.value,
            ModelChoice.OMNIPARSER_O1.value,
            ModelChoice.OMNIPARSER_O3MINI.value,
            ModelChoice.OMNIPARSER_R1.value,
            ModelChoice.OMNIPARSER_QWEN25VL.value,
            ModelChoice.OMNIPARSER_GPT4O_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_O1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_O3MINI_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_GPT4O_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_O1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_O3MINI_ORCHESTRATED.value,
        ]
    ):
        actor = VLMAgent(
            model=model,
            provider=provider,
            api_key=api_key,
            api_response_callback=api_response_callback,
            output_callback=output_callback,
            max_tokens=max_tokens,
            only_n_most_recent_images=only_n_most_recent_images,
        )
    elif model in set(
        [
            ModelChoice.OMNIPARSER_GPT4O_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_O1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_O3MINI_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_R1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_QWEN25VL_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_GPT4O_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_O1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_O3MINI_ORCHESTRATED.value,
        ]
    ):
        actor = VLMOrchestratedAgent(
            model=model,
            provider=provider,
            api_key=api_key,
            api_response_callback=api_response_callback,
            output_callback=output_callback,
            max_tokens=max_tokens,
            only_n_most_recent_images=only_n_most_recent_images,
            save_folder=save_folder,
        )
    else:
        raise ValueError(f"Model {model} not supported")
    executor = AnthropicExecutor(
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
    )
    print(f"Model Inited: {model}, Provider: {provider}")

    tool_result_content = None

    print(f"Start the message loop. User messages: {messages}")

    if model == ModelChoice.CLAUDE_SONNET.value:  # Anthropic loop
        while True:
            parsed_screen = omniparser_client()  # parsed_screen: {"som_image_base64": dino_labled_img, "parsed_content_list": parsed_content_list, "screen_info"}
            screen_info_block = TextBlock(
                text="Below is the structured accessibility information of the current UI screen, which includes text and icons you can operate on, take these information into account when you are making the prediction for the next action. Note you will still need to take screenshot to get the image: \n"
                + parsed_screen["screen_info"],
                type="text",
            )
            screen_info_dict = {"role": "user", "content": [screen_info_block]}
            messages.append(screen_info_dict)
            tools_use_needed = actor(messages=messages)

            for message, tool_result_content in executor(tools_use_needed, messages):
                yield message

            if not tool_result_content:
                return messages

            messages.append({"content": tool_result_content, "role": "user"})

    elif model in set(
        [
            ModelChoice.OMNIPARSER_GPT4O.value,
            ModelChoice.OMNIPARSER_O1.value,
            ModelChoice.OMNIPARSER_O3MINI.value,
            ModelChoice.OMNIPARSER_R1.value,
            ModelChoice.OMNIPARSER_QWEN25VL.value,
            ModelChoice.OMNIPARSER_GPT4O_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_O1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_O3MINI_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_GPT4O_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_O1_ORCHESTRATED.value,
            ModelChoice.OMNIPARSER_AZURE_O3MINI_ORCHESTRATED.value,
        ]
    ):
        while True:
            parsed_screen = omniparser_client()
            tools_use_needed, vlm_response_json = actor(
                messages=messages,
                parsed_screen=parsed_screen,
            )

            for message, tool_result_content in executor(tools_use_needed, messages):
                yield message

            if not tool_result_content:
                return messages
