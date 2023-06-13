import subprocess
from typing import List


def execute_no_trace(command: List[str]) -> str:
    """Executes a command without printing the trace."""
    output = subprocess.Popen(command, stdout=subprocess.PIPE)
    console_output = output.communicate()[0].decode("utf-8")
    return console_output
