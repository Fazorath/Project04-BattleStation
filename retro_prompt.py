from rich.prompt import Prompt

def retro_prompt(prompt_str, choices=None, default=None):
    """
    A unified retro-style prompt for all user input.
    Args:
        prompt_str (str): The prompt string (should include retro color markup).
        choices (list, optional): List of valid choices.
        default (str, optional): Default value.
    Returns:
        str: The user's choice.
    """
    return Prompt.ask(prompt_str, choices=choices, default=default)
