![Alt text](images/MindFlowHeader.png)

Inspired by the need for a more efficient and intelligent way to search code, conversations, and documentation we created MindFlow, the search engine powered by ChatGPT.

## What it MindFlow
MindFlow is a command-line tool and Visual Studio Code Extension (Currently under development) for intelligent development and collaboration. It allows users to generate an index of their work and ask questions about/with it, using a powerful language model (ChatGPT) to provide insightful responses. With MindFlow, you can stay on top of their projects and collaborate with others more effectively.

## Features
- **Note:** MindFlow is currently in beta. How do you want MindFlow to work? Let us know! We are working on adding more features and improving the user experience. If you have any feedback, please leave an issue on the GitHub repo or join our Discord server (https://discord.gg/kfVxeNET). 
- **Note:** Currently, we are awaiting reliable API access to ChatGPT. In the meantime, the responses are not prompts that will be copied to your clipboard which you must then paste into ChatGPT (https://chat.openai.com/chat).

- `mf(r) ask <PROMPT>`:                            
    - ChatGPT in the command line. Use as normal!
- `mf(r) diff [<git diff args>]`:                  
    - Runs a git diff command and summarizes the changes.
- `mf(r) generate [<Files + Folders>]`:            
    - Generates an index of files and folders in the MindFlow server.
- `mf(r) query <YOUR QUERY> [<Files + Folders>]`:  
    - Queries files and folders using generated index. Can generate index with [-i] flag.

## Setup
- **Python:**
    - `pip install mindflow`
    - Binding: mf

- **Rust:**
    - `cargo install mindflow`
    - Binding: mfr
    - (Faster, but requires Rust to be installed (https://www.rust-lang.org/tools/install))  

**Authenticating with MindFlow:**

2 Types of JWT Authentication - Only one is required:

- **OpenAI Auth**
    - Create an OpenAI account (https://beta.openai.com/signup)
    - Create an API key (https://beta.openai.com/account/api-keys)

- **Mindflow Server Auth** (OUT OF ORDER) 
    - While our server is currently in beta, you can request a token in our Discord server (https://discord.gg/kfVxeNET) or by leaving an issue on the GitHub repo.

- Once you have a JWT auth token:
    - Python: `mf auth <TOKEN>`
    - Rust:   ```mfr auth <TOKEN>``` 

## What's next for MindFlow
In the future, MindFlow plans on becoming an even more integral part of the modern developer's toolkit. We plan on adding the ability to ditch traditional documentation and instead integrate directly with your private documents and communication channels, allowing for a more seamless and intuitive experience. With MindFlow, you can have a true "stream of consciousness" with your code, documentation, and communication channels, making it easier than ever to stay on top of your projects and collaborate with your team. We are excited to continue pushing the boundaries of what's possible with language models and revolutionize the way developers work.
