use clap::{Parser, ArgAction};

use crate::command_helpers::diff::generate_diff_prompt;
use crate::requests::prompt::request_prompt;
use crate::utils::response::handle_response_text;

#[derive(Parser)]
pub(crate) struct Diff {
    pub(crate) diff_args: Vec<String>,
    #[arg(short = 'p', long = "prompt", action = ArgAction::SetTrue, value_name = "Get prompt to enter into ChatGPT.")]
    pub(crate) return_prompt: bool,
    #[arg(short = 's', long = "skip-clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) skip_clipboard: bool,
}

impl Diff {
    pub(crate) async fn execute(&mut self) {
        let client = reqwest::Client::new();

        let prompt = generate_diff_prompt(&self.diff_args).await;
        let request_prompt_response = request_prompt(&client, prompt, self.return_prompt).await;   
        handle_response_text(request_prompt_response.text, self.skip_clipboard);
    }
}
