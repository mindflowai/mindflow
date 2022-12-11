from mindflow.utils.response import get_response
from mindflow.utils.exceptions.index_failure import FailureToTrimFiles, IndexGenerationFailure

from typing import List

import os
import json
import chardet
import hashlib

import git

MAX_INDEX_RETRIES = 3


class ResolverIndex:

    def __init__(self, model):
        self.model = model

    def generate_single_index(self, file):
        file_contents = open(file, encoding="utf-8", errors="ignore").read().strip().replace("\n", " ")
        prompt = f"Pretend you are a search engine trying to provide an information rich yet condensed string that can serve as an index for the contents of a file. I want you to respond in as few words as possible while still conveying the contents of this file.\n\n{file_contents}"
        return self._attempt_index_generation(prompt)
    
    def _attempt_index_generation(self, prompt):
        """
        Attempts to generate an index for a file.
        """
        for _ in range(MAX_INDEX_RETRIES):
            try:
                return get_response(self.model, prompt)
            except IndexGenerationFailure:
                pass

        raise IndexGenerationFailure(f"Failed to generate an index after {MAX_INDEX_RETRIES} tries.")
    
    def _get_git_root(self):
        git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        return git_root

    def _get_index_json(self):
        git_root = self._get_git_root()

        if not os.path.exists(os.path.join(git_root, '.mf')):
            os.mkdir(os.path.join(git_root, '.mf'))
            
        # Open the mf_index.json file in read mode
        try:
            with open(os.path.join(git_root, '.mf/index.json'), 'r') as f:
                index = json.load(f)
        except FileNotFoundError: 
            index = {} 

        return index

    def _write_index_json(self, index_json):
        git_root = self._get_git_root()
        
        # write to the json
        with open(os.path.join(git_root, '.mf/index.json'), "w") as file:
            # Write the contents of the dictionary to the JSON file
            json.dump(index_json, file, indent=2, sort_keys=True)

    def generate_all_indexes(self, files: List[str]) -> dict:

        index_json = self._get_index_json()
        
        sub_index = {}
        for file in files:
            with open(file,"rb") as f:
                bytes = f.read() # read entire file as bytes
                file_hash = hashlib.sha256(bytes).hexdigest()

            if file not in index_json or file_hash != index_json[file]['hash']: 
                try: 
                    index_description = self.generate_single_index(file)
                    if index_description:
                        index_json[file] = {'index': index_description, "hash": file_hash}
                        print("Index generated for file: ", file)
                        
                except IndexGenerationFailure as failure:
                    print(failure.message)

            sub_index[file] = index_json[file] if file in index_json else None

        self._write_index_json(index_json)
        return sub_index