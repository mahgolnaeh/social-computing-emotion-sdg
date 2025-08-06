from src.utils.model_loader import get_model_config

# Model selection for different tasks
MODELS = {
    "generation": "openai/gpt-4.1-mini",
    "sdg_classification":"anthropic/claude-opus-4.1",
    "classification": "openai/gpt-4.1-mini",
    "emotion_detection": "anthropic/claude-3.5-sonnet",
    "support": "anthropic/claude-sonnet-4",
    "response_generation": "openai/gpt-4-turbo",
    "test":"mistralai/mistral-7b-instruct"# Future module
}

# Default model (for backward compatibility)
ACTIVE_MODEL = MODELS["response_generation"]

# Get configurations for all models
MODEL_CONFIGS = {
    task: get_model_config(model)
    for task, model in MODELS.items()
}

# Task-specific parameters
TASK_PARAMS = {
    "generation": {
        "temperature": 0.8,
        "top_p": 0.9,
        "max_tokens": 1000
    },
    "sdg_classification": {
        "temperature": 0.1,  # More deterministic
        "top_p": 0.95,
        "max_tokens":512  # Adjusted for SDG classification
    },
    "classification": {
        "temperature": 0.1,  # More deterministic
        "top_p": 0.9,
        "max_tokens":100
    },
    "emotion_detection": {
        "temperature": 0.4,  # Very deterministic
        "top_p": 0.9,
        "max_tokens": 100,
        "response_format": "json"
    },
    "support": {
        "temperature": 0.7,
        "max_tokens": 500,
    },
    "response_generation":{
        "temperature": 0.7,
        "max_tokens": 300,
        "top_p": 1,
        "presence_penalty": 0.5,
        "frequency_penalty": 0.3
    }
}





def get_model_and_params(task: str):
    """Get model name and parameters for a specific task"""
    if task not in MODELS:
        raise ValueError(f"Unknown task: {task}")

    return MODELS[task], TASK_PARAMS.get(task, {})


