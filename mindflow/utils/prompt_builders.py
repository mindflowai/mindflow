from typing import Dict
from typing import List


def build_context_prompt(context: str, text: str) -> List[Dict]:
    return [{"role": "system", "content": context}, {"role": "user", "content": text}]
