![Alt text](images/MindFlowHeader.png)

Inspired by the need for a more efficient and intelligent way to search code, conversations, and documentation we created MindFlow, the search engine powered by ChatGPT.

## What it MindFlow
MindFlow allows users to generate an index of documents using a powerful language models to provide insightful responses to questions you may have about your data. It offers a selection of models to play around with with the ability to configure each model.

## Features
- **Note:** MindFlow is currently in beta. How do you want MindFlow to work? Let us know! We are working on adding more features and improving the user experience. If you have any feedback, please leave an issue on the GitHub repo or join our Discord server (https://discord.gg/kfVxeNET). 

- `mf ask <PROMPT>`:                            
    - GPT in the command line. Use as normal!
- `mf config`:
    - Configure your models used to generate indexes, create embeddings, and generate responses.
- `mf diff [<git diff args>]`:                  
    - Runs a git diff command and summarizes the changes.
- `mf index [document paths]`:            
    - Generates an index of documents.
- `mf query [document paths] <YOUR QUERY>`:  
    - Queries documents using generated index. Can generate index with [-i] flag.
- `mf delete [document paths]`:             
    - Deletes generated index documents.
- `mf refresh [document paths]`:            
    - Refreshes documents if they have been changed. Add [-f] flag to force refresh.
- `mf inspect [document paths]`:
    - Inspect your document indices.

## Examples
1. Query
    - Clone this repo and run `mf index mindflow` to index the repo.
    - Run `mf query mindflow "How can I add a new command to this CLI tool? Please show code."` to query the repo.
    - Output to clipboard:

```
To add a new command to this CLI tool, you need to follow these steps:

1. Define a new command in the `Command` enum class.
2. Create a new function that implements the logic for the new command.
3. Add a new argument parser function for the new command.
4. Add a new `get_parsed_cli_args` case for the new command.
5. Update the `cli` function to include the new command in the parser.
6. Call the new function in the `match` statement in the `cli` function.

Here is an example of how to add a new command called `mycommand`:

1. Define a new command in the `Command` enum class:

class Command(Enum):
    ...
    MYCOMMAND = "mycommand"

2. Create a new function that implements the logic for the new command:

def mycommand():
    print("This is my new command!")

3. Add a new argument parser function for the new command:

def mycommand_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This is my new command.",
    )
    return parser.parse_args(sys.argv[2:])

4. Add a new `get_parsed_cli_args` case for the new command:

def get_parsed_cli_args(command: str) -> argparse.Namespace:
    ...
    case Command.MYCOMMAND.value:
        return mycommand_args()
    ...

5. Update the `cli` function to include the new command in the parser:

def cli():
    parser = set_parser()
    args = parser.parse_args()

    command = Command[args.command].value
    args = get_parsed_cli_args(command)

    ...
    parser.add_argument(
        "command",
        choices=Command.__members__,
        help="The command to execute",
    )
    ...

6. Call the new function in the `match` statement in the `cli` function:

def cli():
    ...
    match command:
        ...
        case Command.MYCOMMAND.value:
            mycommand()
        ...
```

2. Diff
    - Run `mf diff` to summarize the changes in the repo.
    - Output to clipboard:


```
There are two sections in the text provided: Examples and Recommended Use. Here are the changes for each file:

README.md:
- Line 19: Changed the order of the arguments for the `mf query` command.
- Lines 26-47: Added an example for the `mf query` command.
- Lines 50-68: Added instructions for the `mf diff` command.
- Lines 70-80: Added a note about recommended use and how to configure the tool.

I hope this helps! Let me know if you have any further questions.
```

## Recommended Use
While this tool is in beta, it is recommended to use the base models, but more will be added in the future. The base models are:
- Query: GPT 3.5 Turbo
- Index: GPT 3.5 Turbo
- Embedding: Text Embedding Ada 001

By running MF config, you can change the models used for each of these tasks. You can also configure the soft token limit. The soft token limit truncated the text to be sent to the GPT apis. When using the index, this means that your index summaries will be created over smaller chunks of texts, which can be useful, because it allows the query mechanism to more selectively choose chunks of text to return. This will also result in longer indexing times, and it will be more expensive, because more requests must be made. The soft token limit can also be configure for the final prompt, which is the query prompt. Fitting more text into the prompt can allow for more context to be used to generate the response, however, sometimes to much context impacts the quality of the response negatively.

## Setup
- **Python:**
    - `pip install mindflow`
    - Binding: mf

**Authenticating with MindFlow:**

- **OpenAI Auth**
    - Create an OpenAI account (https://beta.openai.com/signup)
    - Create an API key (https://beta.openai.com/account/api-keys)

- Once you have an authorization token:
    - Python: `mf config`

## How does it work?
This tool allows you to build an index of text documents and search through them using GPT-based embeddings. The tool takes document paths as input, extracts the text, splits the documents into chunks, summarizes them, and builds a summarization tree. The tool then uses this tree to generate embeddings of the indexed documents and your query, and selects the top text chunks based on the cosine similarity between these embeddings. The generated index can be saved to a JSON file for later reuse, making subsequent searches faster and cheaper.

## What's next for MindFlow
In the future, MindFlow plans on becoming an even more integral part of the modern developer's toolkit. We plan on adding the ability to ditch traditional documentation and instead integrate directly with your private documents and communication channels, allowing for a more seamless and intuitive experience. With MindFlow, you can have a true "stream of consciousness" with your code, documentation, and communication channels, making it easier than ever to stay on top of your projects and collaborate with your team. We are excited to continue pushing the boundaries of what's possible with language models and revolutionize the way developers work.
