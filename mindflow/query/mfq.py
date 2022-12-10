from typing import Set

import re


MFQ_FILE = "_mf_query.mfq"

FILE_REF_REGEXES = [r"(@[\w|\/|\.|\_]+)", r"(@\[.*\])"]

class MindFlowQueryHandler:
    
    def __init__(
        self, 
        user_query: str,
        refs: Set[str],
    ):
        self._validate(user_query, refs)
        self.query = open(list(refs)[0], "r").read()

    def _validate(self, user_query: str, refs: Set[str]):
        hint = f"\n[Hint] Try running: `mf query \"\" {MFQ_FILE}`"

        if len(refs) > 1:
            print(f"If passing the {MFQ_FILE} file, you may not pass other files in the CLI args (got: {len(refs)} files). This is because the {MFQ_FILE} file contains the question and references.")
            print(hint)
            raise exit(1)

        if len(user_query) > 0:
            print(f"If passing the {MFQ_FILE} file, the query string in the CLI args should be empty (got: {user_query}). This is because the {MFQ_FILE} file contains the question and references.")
            print(hint)
            raise exit(1)

    def get_prompt(self):

        # first, we need to scrub all comments from the file (lines that start with `#`)
        self.query = re.sub(r"#.*", "", self.query)

        # then, we need to parse the `@` references in the text
        refs = set()
        for regex in FILE_REF_REGEXES:
            refs.update(re.findall(regex, self.query))
        refs = set(map(lambda x: x[1:], refs))
        print(refs)

        # then we need to create the prompt to feed to the model.
        # for now, let's replace the `@` references with the filename, and then compose the json as normal

        return "HI!"