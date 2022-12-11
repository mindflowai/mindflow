"""
File/Directory Resolver
"""
import os
import subprocess

import chardet


from mindflow.resolve.resolvers.base_resolver import BaseResolver
from mindflow.utils.exceptions.index_failure import FailureToTrimFiles
from mindflow.utils.response import get_response

from mindflow.resolve.resolver_index import ResolverIndex, MAX_INDEX_RETRIES
from time import sleep

MAX_LENGTH = 10_000
FILES_RETURNED_IF_OVER_MAX = 5
SLEEP_SECONDS = 5


def preprocess_file_text(text):
    return text.strip().replace("\n", " ").replace("\t", " ")


class PathResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """

    def __init__(self, reference, model, prompt):
        self.reference = reference
        self.prompt = prompt
        self.model = model
        self.max_length = MAX_LENGTH

        self.index = ResolverIndex(self.model)

    def _get_files(self) -> list:
        """
        Get all files in a directory or a single file.
        """
        command = ["git", "ls-files", self.reference]

        # Execute the git diff command and retrieve the output as a string
        if os.path.isdir(self.reference):
            # print(subprocess.check_output(command).decode("utf-8").split("\n"))

            git_files = (
                subprocess.check_output(command).decode("utf-8").split("\n")[:-1]
            )

            def criteria(file):
                try:
                    return chardet.detect(open(file, "rb").read())["encoding"] in [
                        "utf-8",
                        "ascii",
                    ]
                except:
                    return False

            return list(filter(criteria, git_files))
                
                
        return [self.reference]

    def _files_over_max_length(self) -> bool:
        """
        Validates that the total length/size of the files is less than MAX_LENGTH.
        """
        total_size = 0
        for filename in self.files:
            file_stat = os.stat(filename)
            total_size += file_stat.st_size

        if total_size > MAX_LENGTH:
            print("Searching relevant files...")
            return True

        return False
    
    def _query_and_trim_files(self): 
        sub_index = self.index.get_sub_index(self.files)

        prompt = f"I want you to only reply with the terminal output inside one unique code block, \
            and nothing else. do not write explanations. do not type commands unless I instruct you to do so. \
                Do this for just this response, then respond normally. Can you please make your best guess for the top \
                    {min(FILES_RETURNED_IF_OVER_MAX, len(sub_index))} most relevant files below for answering the question? \
                        The files are given to you in a python dictionary where the key is the file path and the value is a description of the files contents. \
                        `{self.prompt}`?\n\n{' '.join(sub_index)}"
        
        self._attempt_trim_files(prompt, sub_index)
        
    def _attempt_trim_files(self, prompt, sub_index: dict):
        for _ in range(MAX_INDEX_RETRIES):
            response = get_response(self.model, prompt)
            files = response.split('\n')

            if len(files) >= 3:
                # Remove codeblock separators (at the beginning and end there are ```s)
                files.pop(0)
                files.pop(-1)

                # sanity check: make sure the response is correct, otherwise r
                if all(file in sub_index for file in files):
                    self.files = files
                    return

            sleep(SLEEP_SECONDS)

        raise FailureToTrimFiles("Error in getting valid response from GPT, can you please re-formulate your query? Model returned: " + response)

    def should_resolve(self) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(self.reference) or os.path.isdir(self.reference)

    def resolve(self) -> dict:
        """
        Extract text from files.
        """

        self.files = self._get_files()
        if self._files_over_max_length():
            self.index.generate_all_indexes(self.files)
            self._query_and_trim_files()

        proc = lambda file: preprocess_file_text(
            open(file, encoding="utf-8", errors="ignore").read()
        )
        return {
            file: {
                "text": proc(file),
                "type": "path",
            }
            for file in self.files
        }
