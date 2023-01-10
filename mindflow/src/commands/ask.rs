use clap::{Parser, ArgAction};

use crate::{requests::prompt::request_prompt, utils::response::handle_response_text};

#[derive(Parser)]
pub(crate) struct Ask {
    pub(crate) prompt: Vec<String>,
    #[arg(short = 'c', long = "clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) clipboard: bool,
}

impl Ask {
    pub(crate) async fn execute(&mut self) {
        let client = reqwest::Client::new();        

        let request_prompt_response = request_prompt(&client, self.prompt.join(" ")).await;  
        handle_response_text(request_prompt_response.text, self.clipboard);
    }
}
