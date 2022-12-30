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
        .await?
        .json::<UnindexedReferencesResponse>()
        .await?;

    Ok(res)
}