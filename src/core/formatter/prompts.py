def get_sys_prompt(prompt: str):
    try:
        with open(prompt, "r", encoding="utf-8") as f:
            sys_prompt = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"System prompt file not found: {prompt}")

    return sys_prompt
