import subprocess
from typing import List


def execute_no_trace(command: List[str]) -> str:
    """Executes a command without printing the trace."""
    output = subprocess.Popen(command, stdout=subprocess.PIPE)
    return output.communicate()[0].decode("utf-8")
