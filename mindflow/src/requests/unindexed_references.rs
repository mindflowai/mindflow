use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::utils::config::API_LOCATION;

#[derive(Serialize)]
pub(crate) struct UnindexedReferenceRequest {
    pub(crate) hashes: String,
}

#[derive(Deserialize)]
pub(crate) struct UnindexedReferencesResponse {
    pub(crate) unindexed_hashes: Vec<String>,
}

pub(crate) async fn request_unindexed_references(client: &Client, hashes: &Vec<String>) -> Result<UnindexedReferencesResponse, reqwest::Error> {
    let unindexed_references_payload: UnindexedReferenceRequest = UnindexedReferenceRequest {
        hashes: serde_json::to_string(hashes).unwrap(),
    };
    let url = format!("{}/unindexed", API_LOCATION);
    let res = client.post(&url)
        .json(&unindexed_references_payload)
        .send()
        .await?
        .json::<UnindexedReferencesResponse>()
        .await?;

    Ok(res)
}