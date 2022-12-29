use serde::{Serialize};
use reqwest::{Client};
use std::collections::{HashMap};

use crate::utils::config::API_LOCATION;
use crate::utils::reference::Reference;

const INDEX_BATCH_SIZE: usize = 10;

#[derive(Serialize)]
pub(crate) struct IndexReferencesRequest {
    pub(crate) references: String,
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
    
    let index_reference_request: IndexReferencesRequest = IndexReferencesRequest {
        references: serde_json::to_string(&references_to_index).unwrap(),
    };
    let url = format!("{}/index", API_LOCATION);
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
