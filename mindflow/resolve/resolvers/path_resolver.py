"""
File/Directory Resolver
"""
import json
import os
import subprocess

import chardet
import hashlib

import git


from mindflow.resolve.resolvers.base_resolver import BaseResolver
from mindflow.utils.response import get_response

MAX_LENGTH = 20
FILES_RETURNED_IF_OVER_MAX = 5

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
            self.index = self._get_index()
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
    
    def _get_index(self) -> dict:
        git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")

        if not os.path.exists(os.path.join(git_root, '.mf')):
            os.mkdir(os.path.join(git_root, '.mf'))

        # Open the mf_index.json file in read mode
        try:
            with open(os.path.join(git_root, '.mf/index.json'), 'r') as f:
                index = json.load(f)
        except FileNotFoundError: 
            index = {} 
        
        sub_index = {}
        for file in self.files: 
            with open(file,"rb") as f:
                bytes = f.read() # read entire file as bytes
                file_hash = hashlib.sha256(bytes).hexdigest()

            if file not in index or file_hash != index[file]['hash']: 
                ATTEMPTS = 3
                for i in range(ATTEMPTS):
                    try:
                        index[file] = {'index': self._generate_index(file), "hash": file_hash}
                        print("Generated index for file: " + file)
                        break
                    except:
                        if i == ATTEMPTS - 1:
                            raise Exception("Failed to generate index for file: " + file)
                        continue
            
            sub_index[file] = index[file] if file in index else None
        
        # Open the JSON file in write mode
        with open(os.path.join(git_root, '.mf/index.json'), "w") as file:
            # Write the contents of the dictionary to the JSON file
            json.dump(index, file)
            
        return sub_index

    def _generate_index(self, file):
        file_contents = open(file, encoding="utf-8", errors="ignore").read().strip().replace("\n", " ")
        prompt = f"Pretend you are a search engine trying to provide an information rich yet condensed string that can serve as an index for the contents of a file. I want you to respond in as few words as possible while still conveying the contents of this file.\n\n{file_contents}"
        return get_response(self.model, prompt)
    
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
        files_and_index = {}
        for file in self.files:
            if file in self.index:
                files_and_index[file] = self.index[file]
            else:
                files_and_index[file] = ""

        prompt = f"I want you to only reply with the terminal output inside one unique code block, \
            and nothing else. do not write explanations. do not type commands unless I instruct you to do so. \
                Do this for just this response, then respond normally. Can you please make your best guess for the top \
                    {min(self.max_files_if_over_length, len(files_and_index))} most relevant files below for answering the question? \
                        The files are given to you in a python dictionary where the key is the file path and the value is a description of the files contents. \
                        `{self.prompt}`?\n\n{' '.join(files_and_index)}"
        response = get_response(self.model, prompt)

        # Get files from response
        files = response.split('\n')
        
        # Remove codeblock separators
        files.pop(0)
        files.pop()

        self.files = files
        print("Using ", self.files, " to generate response.")
        # print(response)

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
