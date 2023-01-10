use clap::{Parser, ArgAction};

use crate::resolve::resolve::{resolve};
use crate::requests::query::{request_query};
use crate::resolve::generate_index::generate_index;

#[derive(Parser)]
pub(crate) struct Query {
    #[arg(index = 1)]
    pub(crate) query: String,
    #[arg(index = 2)]
    pub(crate) references: Vec<String>,
    #[arg(short = 'i', long = "index", action = ArgAction::SetTrue, value_name = "Specifies whether you want to create an index for the files you query on.")]
    pub(crate) index: bool,
    #[arg(short = 's', long = "skip-response", action = ArgAction::SetTrue, value_name = "Skip response from GPT model.")]
    pub(crate) skip_response: bool,
    #[arg(short = 't', long = "clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) clipboard: bool,
}

impl Query {
    pub(crate) async fn execute(&mut self) {
        // create query request handler
        let client = reqwest::Client::new();

        // Get resolved references and their hashes
        let all_resolved = resolve(&self.references).await;
        let resolved_hashes = all_resolved.iter().filter_map(|resolved| 
            match resolved.text_hash() {
                Some(hash) => Some(hash),
                None => None
            }
        ).collect::<Vec<String>>();

        // Generate index in Mindflow server if specified.
        if self.index {
            println!("Generating index...");
            generate_index(all_resolved).await;
        }

        // Send query to Mindflow server.
        let request_query_response = request_query(&client, self.query.clone(), resolved_hashes).await;
        println!("{}", request_query_response.text);

        // Implement response skip and copy to clipboard later
        if !self.skip_response {
            //println!("{}", query_response.text);
        }
    }
}
