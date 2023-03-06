# MindFlow
![Alt text](images/MindFlowHeader.png)

Inspired by the need for a more efficient and intelligent way to search code, conversations, and documentation we created MindFlow, the search engine powered by ChatGPT.

## What it MindFlow
MindFlow allows users to generate an index of documents using a powerful language models to provide insightful responses to questions you may have about your data. It offers a selection of models to play around with with the ability to configure each model.

## Getting Started

Pre-requisite: You need to create an OpenAI API account, you can do so [here](https://openai.com/blog/openai-api).

1. Run `pip install mindflow`, or you can clone this repo and run `pip install -e path/to/mindflow`.
2. Run `mf login {OPENAI_API_KEY}`, you can find your openAI API key [here](https://platform.openai.com/account/api-keys).
3. Now you're ready to start using MindFlow!

## Basic Usage

### Interact with ChatGPT Using the CLI
Run: `mf ask "Hey, How's it going?"`

### Query Your Code
You can also ask questions about your code repos. Run the following commands in any git repo:

1. `mf index ./` 
    - To index the entire repo, this will go through all files recursively and generate search indexes for them.
    - :warning: Beware! Large code repositories may take a while and have a decent cost. It shouldn't be too expensive for normal repos, try it on a smaller one first.
2. `mf query ./ "Please summarize this repository."`
    - This will take the index you generated in the above step and use it as context for your question!

### Git Diff Summaries
Make some changes to your git repo without staging/committing them. Then, run `mf diff`! You should get a response that looks like this:

```
`mindflow/commands/diff.py` changes:
- Added import statement for `List` and `Tuple` from the `typing` module.
- Added a function `parse_git_diff` that takes in the output of a `git diff` command and returns a list of tuples containing the file name and the diff content.
- Added a function `batch_git_diffs` that takes in the list of tuples returned by `parse_git_diff` and batches them into smaller chunks of diffs that are less than 3000 characters long.
- Modified the `diff` function to use the new `parse_git_diff` and `batch_git_diffs` functions to batch the diffs and send them to the GPT model for processing.

`mindflow/commands/inspect.py` changes:
- Removed the `print` statement that was used to output the result of a database query.The git diff shows changes in two files: `mindflow/commands/diff.py` and `mindflow/commands/inspect.py`.

`mindflow/commands/diff.py` changes:
- Added import statement for `List` and `Tuple` from the `typing` module.
- Added a function `parse_git_diff` that takes in the output of a `git diff` command and returns a list of tuples containing the file name and the diff content.
- Added a function `batch_git_diffs` that takes in the list of tuples returned by `parse_git_diff` and batches them into smaller chunks of diffs that are less than 3000 characters long.
- Modified the `diff` function to use the new `parse_git_diff` and `batch_git_diffs` functions to batch the diffs and send them to the GPT model for processing.

`mindflow/commands/inspect.py` changes:
- Removed the `print` statement that was used to output the result of a database query.
```

## How does it work?
This tool allows you to build an index of text documents and search through them using GPT-based embeddings. The tool takes document paths as input, extracts the text, splits the documents into chunks, summarizes them, and builds a summarization tree. The tool then uses this tree to generate embeddings of the indexed documents and your query, and selects the top text chunks based on the cosine similarity between these embeddings. The generated index can be saved to a JSON file for later reuse, making subsequent searches faster and cheaper.

## What's next for MindFlow
In the future, MindFlow plans on becoming an even more integral part of the modern developer's toolkit. We plan on adding the ability to ditch traditional documentation and instead integrate directly with your private documents and communication channels, allowing for a more seamless and intuitive experience. With MindFlow, you can have a true "stream of consciousness" with your code, documentation, and communication channels, making it easier than ever to stay on top of your projects and collaborate with your team. We are excited to continue pushing the boundaries of what's possible with language models and revolutionize the way developers work.
