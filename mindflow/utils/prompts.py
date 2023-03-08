"""
This file contains the prompts that are used in the CLI.
"""

GIT_DIFF_PROMPT_PREFIX = "The following is a git diff from my code repository. \
    Please thoroughly explain to me in bullet points the changes for each file. \
        Only provide the file name with its bulleted summary and nothing else in the format: \
            {\
                - *file_name*,\
                    - change1 \
                    - change2 \
                    - change3 \
            }\
        with a new line for each file and change."
INDEX_PROMPT_PREFIX = "Pretend you are a search engine trying to provide an information rich \
    yet condensed string that can serve as an index for the contents or the purpose \
    of a file. I want you to respond in as few words as possible while still conveying \
         the full content and purpose of this file."
CHAT_PROMPT_PREFIX = "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."
COMMIT_PROMPT_PREFIX = "Please provide a commit message for the following changes. Only respond with the commit message and nothing else."
PR_TITLE_PREFIX = "Please provide a title for the following pull request using this git diff summary. Only respond with the title and nothing else."
PR_BODY_PREFIX = "Please provide a body for the following pull request using this git diff summary. I want you to keep it high level, and give core \
      themes and reasons for changes. Try to include some titles and bullet points. Only respond with the body and nothing else."
QUERY = "Please answer the following query like a helpful virtual assistant using the context provided below: "
