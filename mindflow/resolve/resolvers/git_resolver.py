import subprocess

from mindflow.resolve.resolvers.base_resolver import BaseResolver

class GitResolver(BaseResolver):
    def __init__(self, reference):
        self.reference = reference

    def resolve(self):
        command = ["git", "diff"]  # TODO: allow args and such
        diff_result = subprocess.check_output(command).decode("utf-8")

        print(diff_result)

        return {
            "#git-diff": {
                "text": diff_result,
                "type": "diff",
            }
        }


    def should_resolve(self):
        # TODO: more support for git stuff
        print(self.reference)
        return self.reference == "git-diff"