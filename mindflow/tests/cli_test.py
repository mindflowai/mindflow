"""
Test the command line interface
"""
import subprocess
from typing import List


def run_cmd(cmd: List[str], skip_response: bool = True):
    """
    Run a command and return the output
    """
    if skip_response:
        cmd = cmd + ["-s"] + ["-t"]

    return subprocess.run(cmd, stdout=subprocess.PIPE, check=True)


def test_diff():
    """
    Call the summarize command with some sample file names
    """
    run_cmd(["mf", "diff", "main.py"])

    # Check that the output is as expected
    # assert summarize_output.stdout == b"The response has been copied to your clipboard!"


def test_query():
    """
    Call the question command with some sample file names
    """
    run_cmd(["mf", "query", "What are the contents of this file?", "main.py"])

    # Check that the output is as expected
    # assert question_output.stdout == b"The response has been copied to your clipboard!"
