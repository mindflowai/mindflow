use serde::{Serialize};
use reqwest::{Client};
use std::collections::{HashMap};

use crate::utils::config::{CONFIG};
use crate::utils::reference::Reference;
       
#[derive(Serialize)]
pub(crate) struct IndexReferencesRequest {
    pub(crate) references: String,
    pub(crate) auth: String
}

impl IndexReferencesRequest {
    pub fn new(references: &Vec<&Reference>) -> IndexReferencesRequest {
        IndexReferencesRequest {
            references: serde_json::to_string(references).unwrap(),
            auth: CONFIG.get_auth_token()
        }
    }
}

pub(crate) async fn request_index_references(client: &Client, data_map: HashMap<String, Reference>, unindexed_hashes: Vec<String>) {
    // Create a vector of size resolved_references.keys() and fill it with None
    let references_to_index: Vec<&Reference> = unindexed_hashes
        .into_iter()
        .filter_map(|k| {
            data_map.get(&k).map(|data| {
                data
            })

        })
        .collect();
    
    let index_reference_request = IndexReferencesRequest::new(&references_to_index);

    let url = format!("{}/index", CONFIG.get_api_location());
    let res = client.post(&url).json(&index_reference_request).send().await;
    match res {
        Ok(_) => {
            log::debug!("Indexed references");
        },
        Err(e) => {
            println!("Could not index packet of unindexed references: {}", e);
        }
    }
}
