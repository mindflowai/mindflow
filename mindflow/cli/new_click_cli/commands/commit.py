import subprocess
from mindflow.commands.diff import diff
from mindflow.settings import Settings
from mindflow.utils.prompts import COMMIT_PROMPT_PREFIX

@click.command(help="")
def commit():
    """
    Commit command.
    """
    settings = Settings()

    response: str = settings.mindflow_models.query(COMMIT_PROMPT_PREFIX, diff(['--cached']))

    command = ["git", "commit", "-m"] + [response]

    # Execute the git diff command and retrieve the output as a string
    subprocess.check_output(command).decode("utf-8")
