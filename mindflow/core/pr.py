
import subprocess
from typing import List
from mindflow.core.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import PR_BODY_PREFIX, PR_TITLE_PREFIX


def run_pr():
    settings = Settings()

    # Determine the name of the default branch
    default_branch = subprocess.check_output(['git', 'symbolic-ref', 'refs/remotes/origin/HEAD']).decode().strip().split('/')[-1]
    diff_output = run_diff((default_branch,))

    pr_title_prompt = build_context_prompt(PR_TITLE_PREFIX, diff_output)
    pr_title = settings.mindflow_models.query.model(pr_title_prompt)

    pr_body_prompt = build_context_prompt(PR_BODY_PREFIX, diff_output)
    pr_body = settings.mindflow_models.query.model(pr_body_prompt)

    print(f"PR Title: {pr_title}")
    print(f"PR Body: {pr_body}")
    create_pull_request(pr_title, pr_body)

def create_pull_request(title, body):
    command: List[str] = ["gh", "pr", "create", "--title", title, "--body", body]
    pr_result = subprocess.check_output(command).decode("utf-8")
    print(pr_result)

