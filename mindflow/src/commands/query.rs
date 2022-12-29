use clap::{Parser, ArgAction};

use crate::resolve::resolve::{resolve};
use crate::requests::query::{request_query};

#[derive(Parser)]
pub(crate) struct Query {
    #[arg(index = 1)]
    pub(crate) query: String,
    #[arg(index = 2)]
    pub(crate) references: Vec<String>,
    #[arg(short = 's', long = "skip-response", action = ArgAction::SetTrue, value_name = "Skip response from GPT model.")]
    pub(crate) skip_response: bool,
    #[arg(short = 't', long = "clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) clipboard: bool,
}

impl Query {
    pub(crate) async fn execute(&mut self) {
        // create query request handler
        let client = reqwest::Client::new();

        let processed_hashes = resolve(&self.references).await;
        let request_query_response = request_query(&client, self.query.clone(), processed_hashes).await;
        match request_query_response {
            Ok(response) => {
                let output = response.text.chars().take(15).collect::<String>();
                println!("{}", output);
            },
            Err(e) => {
                panic!("Error: {}", e);
            }
        };
        if !self.skip_response {
            //println!("{}", query_response.text);
        }
    }
}
