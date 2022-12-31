use std::process;

use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::utils::config::{CONFIG};

#[derive(Serialize)]
pub(crate) struct QueryRequest {
    pub(crate) query_text: String,
    pub(crate) reference_hashes: Vec<String>,
    pub(crate) auth: String
}

impl QueryRequest {
    pub fn new(query_text: String, reference_hashes: Vec<String>) -> QueryRequest {
        QueryRequest {
            query_text: query_text,
            reference_hashes: reference_hashes,
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct QueryResponse {
    pub(crate) text: String,
}

pub(crate) async fn request_query(client:&Client, query_text: String, processed_hashes: Vec<String>) -> Result<QueryResponse, reqwest::Error> {
    let query = QueryRequest::new(query_text, processed_hashes);
    let res = client
        .post(&format!("{}/query", CONFIG.get_api_location()))
        .json(&query)
        .send()
        .await?;
    
    match res.status().as_u16() {
        400 => {
            println!("Invalid authorization token.");
            process::exit(1);
        }
        _ => Ok(res.json::<QueryResponse>().await?)
    }
}