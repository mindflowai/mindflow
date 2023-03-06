def build_context_prompt(context: str, text: str) -> str:
    return [{"role": "system", "content": context},{"role": "user", "content": text}]