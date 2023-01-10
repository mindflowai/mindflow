// This module contains the request to the Mindflow server to index references.

use serde::{Serialize};
use reqwest::{Client};
use std::process;

use crate::utils::config::{CONFIG};
use crate::utils::reference::Reference;
       
#[derive(Serialize)]
pub(crate) struct IndexReferencesRequest {
    pub(crate) references: String,
    pub(crate) auth: String
}

impl IndexReferencesRequest {
    pub fn new(references: Vec<Reference>) -> IndexReferencesRequest {
        IndexReferencesRequest {
            references: serde_json::to_string(&references).unwrap_or_else(|_| {
                println!("Error: Could not serialize hashes to JSON.");
                process::exit(1);
            }),
            auth: CONFIG.get_auth_token()
        }
    }
}

// Send a request to the Mindflow server to index references.
pub(crate) async fn request_index_references(client: &Client, unindexed_references: Vec<Reference>) {
    let index_reference_request = IndexReferencesRequest::new(unindexed_references);

    let url = format!("{}/index", CONFIG.get_api_location());
    let res = client.post(&url).json(&index_reference_request).send().await;
    
    // match server response
    match res {
        Ok(res) => {
            // match status code
            match res.status().as_u16() {
                400 => {
                    println!("Invalid authorization token.");
                    process::exit(1);
                }
                _ => {
                    log::info!("Successfully indexed references.");
                }
            }
        },
        Err(e) => {
            log::error!("Error indexing references: {}", e);
        }
    }
}
