from typing import List
from simple_term_menu import TerminalMenu


def menu(options: List[str], prompt: str):
    print(prompt)
    response = options[TerminalMenu(options).show()]
    print("\033[A\033[2K", end="")
    return response
