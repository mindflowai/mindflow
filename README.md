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
- `mf query <YOUR QUERY> [document paths]`:  
    - Queries documents using generated index. Can generate index with [-i] flag.
- `mf delete [document paths]`:             
    - Deletes generated index documents.
- `mf refresh [document paths]`:            
    - Refreshes documents if they have been changed. Add [-f] flag to force refresh.
- `mf inspect [document paths]`:
    - Inspect your document indices.

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


## What's next for MindFlow
In the future, MindFlow plans on becoming an even more integral part of the modern developer's toolkit. We plan on adding the ability to ditch traditional documentation and instead integrate directly with your private documents and communication channels, allowing for a more seamless and intuitive experience. With MindFlow, you can have a true "stream of consciousness" with your code, documentation, and communication channels, making it easier than ever to stay on top of your projects and collaborate with your team. We are excited to continue pushing the boundaries of what's possible with language models and revolutionize the way developers work.
