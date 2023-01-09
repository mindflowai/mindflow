// Send a request to the Mindflow server to get a list of hashes that are not yet indexed.

use std::process;

use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::utils::config::{CONFIG};

#[derive(Serialize)]
pub(crate) struct UnindexedReferenceRequest {
    pub(crate) hashes: String,
    pub(crate) auth: String
}

impl UnindexedReferenceRequest {
    pub fn new(hashes: Vec<&String>) -> UnindexedReferenceRequest {
        UnindexedReferenceRequest {
            hashes: serde_json::to_string(&hashes).unwrap(),
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct UnindexedReferencesResponse {
    pub(crate) unindexed_hashes: Vec<String>,
}

pub(crate) async fn request_unindexed_references(client: &Client, hashes: Vec<&String>) -> UnindexedReferencesResponse {
    let unindexed_references_payload: UnindexedReferenceRequest  = UnindexedReferenceRequest::new(hashes);
    let url = format!("{}/unindexed", CONFIG.get_api_location());
    let res = client.post(&url)
        .json(&unindexed_references_payload)
        .send()
        .await;

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
                    match res.json().await {
                        Ok(unindexed_references_response) => {
                            return unindexed_references_response
                        }
                        Err(e) => {
                            println!("Error: Could not get unindexed hashes: {}", e);
                            process::exit(1);
                        }
                    }
                }
            }
        },
        Err(e) => {
            println!("Error: Could not get unindexed hashes: {}", e);
            UnindexedReferencesResponse{ unindexed_hashes: Vec::new() }
        }
    }
}
