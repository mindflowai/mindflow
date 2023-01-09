use clap::{Parser, ArgAction};

use crate::requests::prompt::request_prompt;

#[derive(Parser)]
pub(crate) struct Ask {
    pub(crate) prompt: Vec<String>,
    #[arg(short = 's', long = "skip-response", action = ArgAction::SetTrue, value_name = "Skip response from GPT model.")]
    pub(crate) skip_response: bool,
    #[arg(short = 't', long = "clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) clipboard: bool,
}

impl Ask {
    pub(crate) async fn execute(&mut self) {
        let client = reqwest::Client::new();        

        let request_prompt_response = request_prompt(&client, self.prompt.join(" ")).await;  
        println!("{}", request_prompt_response.text);
    }
}
