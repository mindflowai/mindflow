import subprocess
from typing import List


## Execute a command without printing out any additional trace information
def execute_no_trace(command: List[str]) -> str:
    """
    Executes a command without tracing.
    """
    # Execute the command and retrieve the output as a string
    output = subprocess.Popen(command, stdout=subprocess.PIPE)

    # Capture the output and decode it
    console_output = output.communicate()[0].decode("utf-8")

    return console_output
