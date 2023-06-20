import subprocess
from typing import List


def execute_command_and_print_without_trace(command: List[str]) -> str:
    output = subprocess.Popen(command, stdout=subprocess.PIPE)
    return output.communicate()[0].decode("utf-8")
