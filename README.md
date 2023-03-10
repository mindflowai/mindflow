# :brain: MindFlow :ocean:
![Screenshot 2023-03-06 at 1 45 06 AM](https://user-images.githubusercontent.com/26421036/223074441-6cf9707e-f596-4b22-bbcc-78936d578123.png)


Inspired by our hatred for maintaining documentation, we developed MindFlow, a code search engine powered by [ChatGPT](https://openai.com/blog/chatgpt).
MindFlow answers natural language queries about your repos and provides tools for streamlining your developer experience.

We efficiently index your code repo by leveraging hierarchical embeddings and summaries for files/directories. Furthermore, we keep them updated with each file hash so you can save those precious API tokens!

## Support Us!
Please consider supporting us on our [patreon](https://www.patreon.com/MindFlowAI)! :heart:

## Showcase
### Chat Persistence and File Context!
<img width="896" alt="Screenshot 2023-03-09 at 4 02 02 PM" src="https://user-images.githubusercontent.com/26421036/224189205-6d786126-7da4-448e-801d-375ec284a05c.png">

## Getting Started

Pre-requisite: You'll need to create an OpenAI API account; you'll be able to do so [here](https://openai.com/blog/openai-api).

1. Run `pip install mindflow,` or you can clone this repo and run `pip install -e path/to/mindflow`.
2. Run `mf login {OPENAI_API_KEY}`; you can find your OpenAI API key [here](https://platform.openai.com/account/api-keys).
3. Now, you're ready to start using MindFlow!

## Basic Usage

### Chats
There are multiple levels to using mindflow's chat feature.

1. Simplest
- `mf chat "explain what a programming language is"`
    - Interact with chatGPT directly just like on the chatGPT website. We also have chat persistence, so it will remember the previous chat messages.
2. With File Context
- `mf chat "please summarize what this code does" path/to/code.py`
    - You can provide single or multi-file context to chatGPT by passing in any number of files as a separate argument in the `mf chat` call. For sufficiently small files (see: [chatGPT token limits](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)), this will work and also maintain chat history.
3. With Directory Context
- `mf chat "what are these submodules responsible for? path/to/submodule1/ path/to/submodule2/`
    - Providing directories will actually run an indexer over your code subdirectories/files recursively. So it may take a while to fully index everything -- don't worry; we'll warn you if the cost becomes a concern! Right now the warning triggers if the index job costs >$0.50USD.
4. Custom pre-indexed context
- `mf index path/to/subdir/ file1.txt path/to/file2.txt`
- `mf chat -s "How do all of my classes relate to one another?" ./`
    - If you pre-index your repository, you can narrow the scope for the context provided to the chat. Passing `-s` will skip the auto-indexing, and instead will defer to the currently existing index. This index is generated in the first step `mf index` where only those files/subdirs will be included.
    - This can save you time and money if your repository is significantly large.

### Chat History and Persistence
By default, simple chat messages (when referencing no files or very small files) will be stored locally so that you can retain chat persistence. 

To see stats about your chat history, you can run `mf history stats`.

If you want to clear your chat history, you can run `mf history clear` and it will forget all previous messages that you've sent.

If you try adding directories to your chat messages, chat persistence will be disabled, and no previous context will be used. This will change as MindFlow matures, and the openAI API supports more token levels/conversation histories natively.

### Git Diff Summaries
Note: Git diff summaries do not support chat persistence yet.

Make some changes to your git repo without staging/committing them. Then, run `mf diff`! You should get a response that looks like this:

```
`mindflow/commands/diff.py` changes:
- Added import statement for `List` and `Tuple` from the `typing` module.
- Added a function `parse_git_diff` that takes in the output of a `git diff` command and returns a list of tuples containing the file name and the diff content.
- Added a function `batch_git_diffs` that takes in the list of tuples returned by `parse_git_diff` and batches them into smaller chunks of diffs that are less than 3000 characters long.
- Modified the `diff` function to use the new `parse_git_diff` and `batch_git_diffs` functions to batch the diffs and send them to the GPT model for processing.

`mindflow/commands/inspect.py` changes:
- Removed the `print` statement used to output the result of a database query. The git diff shows changes in two files: `mindflow/commands/diff.py` and `mindflow/commands/inspect.py`.

`mindflow/commands/diff.py` changes:
- Added import statement for `List` and `Tuple` from the `typing` module.
- Added a function `parse_git_diff` that takes in the output of a `git diff` command and returns a list of tuples containing the file name and the diff content.
- Added a function `batch_git_diffs` that takes in the list of tuples returned by `parse_git_diff` and batches them into smaller chunks of diffs that are less than 3000 characters long.
- Modified the `diff` function to use the new `parse_git_diff` and `batch_git_diffs` functions to batch the diffs and send them to the GPT model for processing.

`mindflow/commands/inspect.py` changes:
- Removed the `print` statement used to output the result of a database query.
```

### Git Commit With GPT Messages
Make some changes to your git repo and stage them. Then, run `mf commit`! You should get a response that looks like this:

```
[formatting 7770179] Add needs_push() function and check in run_pr() function.
 1 file changed, 14 insertions(+)
```

### Create PRs/MRs With GPT Titles And Body
Make some changes to your branch and stage, and then commit them. Then, run `mf pr` for GitHub or `mf mr` for GitLab! A pull request/merge request should be created with a title and body generated by GPT, and a link to the PR should be printed to the console.
- To use this feature, you must first install and authenticate the [GitHub CLI](https://cli.github.com/).

## How does it work?
This tool allows you to build an index of text documents and search through them using GPT-based embeddings. The tool takes document paths as input, extracts the text, splits the documents into chunks, summarizes them, and builds a summarization tree. The tool then uses this tree to generate embeddings of the indexed documents and your query and selects the top text chunks based on the cosine similarity between these embeddings. The generated index can be saved to a JSON file for later reuse, making subsequent searches faster and cheaper.

## What's next for MindFlow
In the future, MindFlow plans on becoming an even more integral part of the modern developer's toolkit. We plan on adding the ability to ditch traditional documentation and instead integrate directly with your private documents and communication channels, allowing for a more seamless and intuitive experience. With MindFlow, you can have a true "stream of consciousness" with your code, documentation, and communication channels, making it easier than ever to stay on top of your projects and collaborate with your team. We are excited to continue pushing the boundaries of what's possible with language models and revolutionizing how developers work.

## Socials
Follow us on [Twitter](https://twitter.com/mindflow_ai)!
