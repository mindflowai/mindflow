// Send a request to the Mindflow server to get a list of hashes that are not yet indexed.

use std::process;

use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::{utils::config::{CONFIG}, requests::status::error::ErrorResponse};

#[derive(Serialize)]
pub(crate) struct UnindexedReferenceRequest {
    pub(crate) hashes: String,
    pub(crate) auth: String
}

impl UnindexedReferenceRequest {
    pub fn new(hashes: Vec<&str>) -> UnindexedReferenceRequest {
        UnindexedReferenceRequest {
            hashes: serde_json::to_string(&hashes).unwrap_or_else(|_| {
                println!("Error: Could not serialize hashes to JSON.");
                process::exit(1);
            }),
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct UnindexedReferencesResponse {
    pub(crate) unindexed_hashes: Vec<String>,
}

// Send a request to the Mindflow server to get a list of hashes that are not yet indexed.
pub(crate) async fn request_unindexed_references(client: &Client, hashes: Vec<&str>) -> UnindexedReferencesResponse {
    let unindexed_references_payload: UnindexedReferenceRequest  = UnindexedReferenceRequest::new(hashes);
    let url = format!("{}/unindexed", CONFIG.get_api_location());
    let res = match client.post(&url)
        .json(&unindexed_references_payload)
        .send()
        .await {
            Ok(res) => res,
            Err(_e) => { 
                println!("Error: Could not get unindexed hashes");
                process::exit(1) 
            },
        };

    // match status code
    match res.status().as_u16() {
        200 => {
            match res.json().await {
                Ok(unindexed_references_response) => {
                    unindexed_references_response
                }
                Err(e) => {
                    println!("Error: Could not get unindexed hashes: {}", e);
                    process::exit(1);
                }
            }
        }
        status   => {
            let error: ErrorResponse = res.json().await.unwrap_or_else(|_| {
                println!("Error: Could not parse error response.");
                process::exit(1);
            });
            println!("Error: {} - {}", status, error.msg);
            process::exit(1);
        }
    }
}
