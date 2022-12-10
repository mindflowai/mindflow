from typing import Set


MFQ_FILE = "_mf_query.mfq"


class MindFlowQueryHandler:
    
    def __init__(
        self, 
        user_query: str,
        refs: Set[str],
    ):
        self.user_query = user_query
        self.refs = refs

        self._validate()

    def _validate(self):
        hint = f"\n[Hint] Try running: `mf query \"\" {MFQ_FILE}`"

        if len(self.refs) > 1:
            print(f"If passing the {MFQ_FILE} file, you may not pass other files in the CLI args. This is because the {MFQ_FILE} file contains the question and references.")
            print(hint)
            raise exit(1)

        if len(self.user_query) > 0:
            print(f"If passing the {MFQ_FILE} file, the query string in the CLI args should be empty. This is because the {MFQ_FILE} file contains the question and references.")
            print(hint)
            raise exit(1)