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
    pub fn new(hashes: &Vec<String>) -> UnindexedReferenceRequest {
        UnindexedReferenceRequest {
            hashes: serde_json::to_string(hashes).unwrap(),
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct UnindexedReferencesResponse {
    pub(crate) unindexed_hashes: Vec<String>,
}

pub(crate) async fn request_unindexed_references(client: &Client, hashes: &Vec<String>) -> Result<UnindexedReferencesResponse, reqwest::Error> {
    let unindexed_references_payload: UnindexedReferenceRequest  = UnindexedReferenceRequest::new(hashes);
    let url = format!("{}/unindexed", CONFIG.get_api_location());
    let res = client.post(&url)
        .json(&unindexed_references_payload)
        .send()
        .await;

    // Through error if 400 status
    match res {
        Ok(res) => {
            match res.status().as_u16() {
                400 => {
                    println!("Invalid authorization token.");
                    process::exit(1);
                }
                _ => {
                    let unindexed_references_response: UnindexedReferencesResponse = res.json().await.unwrap();
                    Ok(unindexed_references_response)
                }
            }
        },
        Err(err) => Err(err)
    }
}