use clap::{Parser, ArgAction};

use crate::command_helpers::diff::generate_diff_prompt;
use crate::requests::prompt::request_prompt;

#[derive(Parser)]
pub(crate) struct Diff {
    pub(crate) diff_args: Vec<String>,
    #[arg(short = 's', long = "skip-response", action = ArgAction::SetTrue, value_name = "Skip response from GPT model.")]
    pub(crate) skip_response: bool,
    #[arg(short = 't', long = "clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) clipboard: bool,
}

impl Diff {
    pub(crate) async fn execute(&mut self) {
        let client = reqwest::Client::new();

        let prompt = generate_diff_prompt(&self.diff_args).await;
        let request_prompt_response = request_prompt(&client, prompt).await;   
        
        match request_prompt_response {
            Ok(response) => {
                println!("{}", response.text);
            },
            Err(e) => {
                panic!("Error: {}", e);
            }
        };
    }
}
