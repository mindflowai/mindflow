import subprocess

from mindflow.cli.new_click_cli.commands.diff import diff
from mindflow.settings import Settings
from mindflow.utils.prompts import COMMIT_PROMPT_PREFIX

def run_commit():
    """
    Commit command.
    """
    settings = Settings()

    print("Generating commit message...")
    response: str = settings.mindflow_models.query(COMMIT_PROMPT_PREFIX, diff())

    command = ["git", "commit", "-m"] + response

    # Execute the git diff command and retrieve the output as a string
    subprocess.check_output(command).decode("utf-8")