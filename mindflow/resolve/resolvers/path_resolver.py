"""
File/Directory Resolver
"""
import os
import subprocess

import chardet
import Levenshtein

from mindflow.resolve.resolvers.base_resolver import BaseResolver
from mindflow.utils.response import get_response

MAX_LENGTH = 20_000
FILES_RETURNED_IF_OVER_MAX = 3

class PathResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """

    def __init__(self, reference, model, prompt):
        self.reference = reference
        self.prompt = prompt
        self.model = model
        self.max_length = MAX_LENGTH
        self.max_files_if_over_length = FILES_RETURNED_IF_OVER_MAX
        self.files = self._get_files()
        if self._files_over_max_length():
            self._query_and_trim_files()

    def _get_files(self) -> list:
        """
        Get all files in a directory or a single file.
        """
        command = ["git", "ls-files", self.reference]

        # Execute the git diff command and retrieve the output as a string
        if os.path.isdir(self.reference):
            #print(subprocess.check_output(command).decode("utf-8").split("\n"))
    
            git_files = subprocess.check_output(command).decode("utf-8").split("\n")[:-1]
            
            def criteria(file): 
                try:
                    return chardet.detect(open(file, "rb").read())["encoding"] in ["utf-8", "ascii"]
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
        """
        
        """
        prompt = f"Can you please make your best guess for the top 3 most relevant files below for answering the question `{self.prompt}`?\n\n{' '.join(self.files)}"
        response = get_response(self.model, prompt)

        levenshteins = []
        for file in self.files: 
            levenshteins.append(Levenshtein.distance(file, response))
        
        # Get index and value for each element in the list of Levenshtein distances
        indexed_list = list(enumerate(levenshteins))

        # Sort the list of tuples by the value in descending order
        sorted_list = sorted(indexed_list, key=lambda x: x[1], reverse=True)

        # Take the first three elements of the sorted list
        top_indices = [x[0] for x in sorted_list[:min(self.max_files_if_over_length, len(self.files))]]

        self.files = [self.files[i] for i in top_indices]

    def should_resolve(self) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(self.reference) or os.path.isdir(self.reference)

    def resolve(self) -> dict:
        """
        Extract text from files.
        """
        return {
            file: {
                "text": open(file, encoding="utf-8", errors="ignore")
                .read()
                .strip()
                .replace("\n", " "),
                "type": "path",
            }
            for file in self.files
        }
