use clap::{Parser, ArgAction};

use crate::resolve_handling::resolve::resolve;
use crate::requests::query::request_query;
use crate::resolve_handling::generate_index::generate_index;
use crate::utils::response::handle_response_text;


#[derive(Parser)]
pub(crate) struct Query {
    #[arg(index = 1)]
    pub(crate) query: String,
    #[arg(index = 2)]
    pub(crate) references: Vec<String>,
    #[arg(short = 'i', long = "index", action = ArgAction::SetTrue, value_name = "Specifies whether you want to create an index for the files you query on.")]
    pub(crate) index: bool,
    #[arg(short = 'c', long = "clipboard", action = ArgAction::SetTrue, value_name = "Copy response to clipboard.")]
    pub(crate) clipboard: bool,
}

impl Query {
    pub(crate) async fn execute(&mut self) {
        // create query request handler
        let client = reqwest::Client::new();

        // Get resolved references and their hashes
        let all_resolved = resolve(&self.references).await;
        let resolved_hashes = all_resolved.iter().filter_map(|resolved| 
            resolved.text_hash()
        ).collect::<Vec<String>>();

        // Generate index in Mindflow server if specified.
        if self.index {
            println!("Generating index...");
            generate_index(all_resolved).await;
        }

        // Send query to Mindflow server.
        let request_query_response = request_query(&client, self.query.clone(), resolved_hashes).await;
        handle_response_text(request_query_response.text, self.clipboard);
    }
}
