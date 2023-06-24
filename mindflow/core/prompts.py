"""This file contains the prompts that are used in the CLI."""

GIT_DIFF_PROMPT_PREFIX = "The following is a git diff from my code repository. \
    Please thoroughly explain to me in bullet points the changes for each file. \
        In your response back to me, only provide the file name with its bulleted summary indented once and nothing else in the format:\n \
            \
            - *file_name*:\n \
                - change1\n \
                - change2\n \
                - change3\n \
            \
        with a new line for each file and change. Your entire response should be bulleted like just mentioned with no additional text."
INDEX_PROMPT_PREFIX = "Pretend you are a search engine trying to provide an information rich \
    yet condensed string that can serve as an index for the contents or the purpose \
    of a file. I want you to respond in as few words as possible while still conveying \
         the full content and purpose of this file."
CHAT_PROMPT_PREFIX = "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."
COMMIT_PROMPT_PREFIX = "Please provide a commit message for the following changes. Only respond with a single commit message and nothing else. Put the response within XML tage like <COMMIT></COMMIT>."
PR_TITLE_PREFIX = "Please provide a title for the following pull request using this git diff summary. Only respond with the title and nothing else."
PR_BODY_PREFIX = "Please provide a body for the following pull request using this git diff summary. I want you to keep it high level, and give core \
      themes and reasons for changes. Try to include some titles and bullet points. Only respond with the body and nothing else."
QUERY_PROMPT_PREFIX = "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."
DEFAULT_CONVERSATION_SYSTEM_PROMPT = "You are a senior software engineer responding to another software engineer's chat messages regarding your codebase, make sure to be polite and helpful, and provide thorough answers with example code when necessary."
GIT_DIFF_SUMMARIZE_PROMPT = 'What is the higher level purpose of these changes? Keep it short and sweet, don\'t provide any useless or redundant information like "made changes to the code". Do NOT speak in generalities about the higher level changes, be specific.'
