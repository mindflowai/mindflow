use std::collections::{HashMap};
use indicatif::{ProgressBar, ProgressStyle};

use rayon::prelude::*;

use reqwest::Client;
use tokio::task::spawn_blocking;

use crate::requests::unindexed_references::{request_unindexed_references};
use crate::requests::index_references::{request_index_references};
use crate::resolve::file_path_resolver::ResolvedFilePath;
use crate::resolve::resolver_trait::Resolved;
use crate::utils::reference::Reference;

const PACKET_SIZE: u64 = 2 * 1024 * 1024;

pub async fn generate_index(resolved_paths: Vec<ResolvedFilePath>) -> Vec<String> {
    let client = Client::new();
    let mut processed_hashes: Vec<String> = Vec::new();
    
    let sizes: Vec<u64> = resolved_paths
        .par_iter()
        .filter_map(|resolved_path| {
            resolved_path.size_bytes()
        })
        .collect();

    let mut packets: Vec<Vec<ResolvedFilePath>> = Vec::new();
    let mut packet: Vec<ResolvedFilePath> = Vec::new();

    let mut packet_size: u64 = 0;
    let mut total_size = 0;

    for (resolved_path, resolved_size) in resolved_paths.into_iter().zip(sizes) {
        if resolved_size > PACKET_SIZE {
            println!("LARGE FILE: {}", resolved_path.path);
            continue
        }
        if packet_size + resolved_size <= PACKET_SIZE {
            packet.push(resolved_path);
            packet_size += resolved_size;
        } else {
            packets.push(packet);
            packet = vec![resolved_path];
            total_size += packet_size;
            packet_size = resolved_size;
        }
    }

    if !packet.is_empty() {
        total_size += packet_size;
        packets.push(packet);
    }

    let pb = ProgressBar::new(packets.len() as u64);
    pb.set_style(ProgressStyle::default_bar());
    pb.set_message("Indexing files");
    let mut packet_index = 0;

    for packet in packets {
        let result = spawn_blocking( move || {
            let reference_vec: Vec<Reference> = packet
                .par_iter()
                .filter_map(|resolved_path| {
                    resolved_path.create_reference()
                })
                .collect();
            reference_vec
        }).await.unwrap();

        let mut hashes: Vec<String> = Vec::new();
        let mut data_map: HashMap<String, Reference> = HashMap::new();

        for reference in result {
            hashes.push(reference.hash.clone());
            data_map.insert(reference.hash.clone(), reference);
        }

        let unindexed_reference_response = request_unindexed_references(&client, &hashes).await;
        let unindexed_hashes = match unindexed_reference_response {
            Ok(unindexed_reference_response) => unindexed_reference_response.unindexed_hashes,
            Err(e) => {
                println!("Error: Could not get unindexed hashes: {}", e);
                Vec::new()
            }
        };
        if unindexed_hashes.len() != 0 {
            request_index_references(&client, data_map, unindexed_hashes).await;
        }

        packet_index += 1;
        pb.set_position(packet_index);


        processed_hashes.extend(hashes);
    }
    println!("Total content size: MB {}\n", format!("{:.2}", total_size as f64 / 1024.0 / 1024.0));
    processed_hashes
}