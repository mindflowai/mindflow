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
Run: `mf ask "What is quantum physics?"`. You should get a response like this:

```
Quantum physics is the branch of physics that studies the behavior of matter and energy at the scale of atoms and subatomic particles. It is a fundamental theory that describes the laws of nature governing the behavior of matter and energy at the smallest scales. In contrast to classical physics, which describes the behavior of macroscopic objects, quantum physics deals with the properties of individual particles, such as electrons, protons, and photons, and how they interact with each other.

One of the most important concepts in quantum physics is the idea of superposition, which states that a particle can exist in multiple states or locations simultaneously. Another key concept is entanglement, which refers to the quantum mechanical phenomenon where two particles can become correlated in such a way that the state of one particle is dependent on the state of the other, no matter how far apart they are.

Quantum physics has many practical applications in fields such as electronics, computing, and cryptography, and it has revolutionized our understanding of the physical world. However, it also challenges our classical intuition and requires a new way of thinking about the nature of reality.
```

### Query Your Code
You can also ask questions about your code repos. Run the following commands in any git repo:

1. `mf index ./` 
    - To index the entire repo, this will go through all files recursively and generate search indexes for them.
    - :warning: Beware! Large code repositories may take a while and have a decent cost. It shouldn't be too expensive for normal repos, try it on a smaller one first.
2. `mf query ./ "Please summarize this repository."`
    - This will take the index you generated in the above step and use it as context for your question!

You should see a response that looks something like this:


```
This is a Python file containing various functions and commands for the MindFlow CLI (Command Line Interface). It includes commands such as `ask`, `commit`, `config`, `delete`, `diff`, `index`, `inspect`, `query`, and `refresh`. The `ask` command is used to generate a prompt and then use it as a prompt for GPT bot. The `commit` command is used to generate a git commit response by feeding git diff to GPT. The `config` command is used to configure a model. The `delete` command is used to delete a document from the MindFlow index. The `diff` command is used to show the difference between two git commits. The `index` command is used to create or update the MindFlow index. The `inspect` command is used to inspect the MindFlow index. The `query` command is used to run a query against the MindFlow index. The `refresh` command is used to refresh the MindFlow index.
```

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
