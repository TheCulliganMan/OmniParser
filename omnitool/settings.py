"""Settings for the OmniTool application."""

from enum import Enum

class ModelChoice(str, Enum):
    OMNIPARSER_GPT4O = "omniparser + gpt-4o"
    OMNIPARSER_O1 = "omniparser + o1"
    OMNIPARSER_O3MINI = "omniparser + o3-mini"
    OMNIPARSER_R1 = "omniparser + R1"
    OMNIPARSER_QWEN25VL = "omniparser + qwen2.5vl"
    CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
    OMNIPARSER_GPT4O_ORCHESTRATED = "omniparser + gpt-4o-orchestrated"
    OMNIPARSER_O1_ORCHESTRATED = "omniparser + o1-orchestrated"
    OMNIPARSER_O3MINI_ORCHESTRATED = "omniparser + o3-mini-orchestrated"
    OMNIPARSER_R1_ORCHESTRATED = "omniparser + R1-orchestrated"
    OMNIPARSER_QWEN25VL_ORCHESTRATED = "omniparser + qwen2.5vl-orchestrated"
    # Azure models
    OMNIPARSER_AZURE_GPT4O_ORCHESTRATED = "omniparser + azure-gpt-4o-orchestrated"
    OMNIPARSER_AZURE_O1_ORCHESTRATED = "omniparser + azure-o1-orchestrated"
    OMNIPARSER_AZURE_O3MINI_ORCHESTRATED = "omniparser + azure-o3-mini-orchestrated"

class InternalModelName(str, Enum):
    GPT4O = "gpt-4o-2024-11-20"
    O1 = "o1"
    O3MINI = "o3-mini"
    R1 = "deepseek-r1-distill-llama-70b"
    QWEN25VL = "qwen2.5-vl-72b-instruct"
    CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
    # Azure models
    AZURE_GPT4O = "gpt-4o"
    AZURE_O1 = "o1"
    AZURE_O3MINI = "o3-mini"

# Mapping from display names to internal model names
MODEL_DISPLAY_TO_INTERNAL = {
    ModelChoice.OMNIPARSER_GPT4O: InternalModelName.GPT4O,
    ModelChoice.OMNIPARSER_O1: InternalModelName.O1,
    ModelChoice.OMNIPARSER_O3MINI: InternalModelName.O3MINI,
    ModelChoice.OMNIPARSER_R1: InternalModelName.R1,
    ModelChoice.OMNIPARSER_QWEN25VL: InternalModelName.QWEN25VL,
    ModelChoice.CLAUDE_SONNET: InternalModelName.CLAUDE_SONNET,
    ModelChoice.OMNIPARSER_GPT4O_ORCHESTRATED: InternalModelName.GPT4O,
    ModelChoice.OMNIPARSER_O1_ORCHESTRATED: InternalModelName.O1,
    ModelChoice.OMNIPARSER_O3MINI_ORCHESTRATED: InternalModelName.O3MINI,
    ModelChoice.OMNIPARSER_R1_ORCHESTRATED: InternalModelName.R1,
    ModelChoice.OMNIPARSER_QWEN25VL_ORCHESTRATED: InternalModelName.QWEN25VL,
    # Azure orchestrated models
    ModelChoice.OMNIPARSER_AZURE_GPT4O_ORCHESTRATED: InternalModelName.AZURE_GPT4O,
    ModelChoice.OMNIPARSER_AZURE_O1_ORCHESTRATED: InternalModelName.AZURE_O1,
    ModelChoice.OMNIPARSER_AZURE_O3MINI_ORCHESTRATED: InternalModelName.AZURE_O3MINI,
}

# List of all model choices for UI dropdowns
MODEL_CHOICES = [choice.value for choice in ModelChoice]

AZURE_OPENAI_URL = "https://YOUR_AZURE_OPENAI_RESOURCE_NAME.openai.azure.com/"
AZURE_OPENAI_API_VERSION = "2024-10-21"
AZURE_OPENAI_SCOPE = "https://cognitiveservices.azure.com/.default"

# Default provider and model
DEFAULT_PROVIDER = "azure-openai"
DEFAULT_MODEL = ModelChoice.OMNIPARSER_GPT4O.value
