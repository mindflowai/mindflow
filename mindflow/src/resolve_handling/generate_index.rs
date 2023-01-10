use std::collections::{HashMap};
use indicatif::{ProgressBar, ProgressStyle};

use rayon::prelude::*;

use reqwest::Client;
use tokio::task::spawn_blocking;

use crate::requests::unindexed_references::{request_unindexed_references};
use crate::requests::index_references::{request_index_references};
use crate::utils::reference::Reference;

use super::resolve::Resolved;

// The maximum number of bytes that can be sent in a single request.
const PACKET_SIZE: u64 = 2 * 1024 * 1024;

// Checks if the references are indexed and if not, indexes them.
pub async fn generate_index(resolved_paths: Vec<Resolved>) {
    let client = Client::new();

    let packets = create_packets(resolved_paths);
    let pb = create_progress_bar(packets.len() as u64);

    for (packet_index, packet) in packets.into_iter().enumerate() {
        // Limits the number of packets whose text is loaded into memory at once.
        let references_hash_map: HashMap<String, Reference> = resolve_packet_to_references(packet).await.into_iter().map(|reference| {
            (reference.hash.clone(), reference)
        }).collect();

        // Get the hashes of the references that are not indexed and index them.
        let reference_hash_map_keys =references_hash_map.keys().map(|key| key.as_str()).collect();
        let unindexed_hashes = request_unindexed_references(&client, reference_hash_map_keys).await.unindexed_hashes;
        if !unindexed_hashes.is_empty() {
            let unindexed_references = filter_unindexed_references(references_hash_map, unindexed_hashes);
            request_index_references(&client, unindexed_references).await;
        }

        // Update progress.
        pb.set_position(packet_index as u64);
    }
}

fn filter_unindexed_references(references_hash_map: HashMap<String, Reference>, unindexed_hashes: Vec<String>) -> Vec<Reference> {
    unindexed_hashes.into_iter()
        .filter_map(|k| {
            references_hash_map.get(k.as_str()).map(|data| {
                data.to_owned()
            })

        }).collect()
}

// Break references into packets of size PACKET_SIZE and send them to the server.
fn create_packets(all_resolved: Vec<Resolved>) -> Vec<Vec<Resolved>> {
    let sizes: Vec<u64> = all_resolved
        .par_iter()
        .filter_map(|resolved| {
            resolved.size_bytes()
        })
        .collect();

    let mut packets: Vec<Vec<Resolved>> = Vec::new();
    let mut packet: Vec<Resolved> = Vec::new();

    let mut packet_size: u64 = 0;
    let mut total_size = 0;

    for (resolved, resolved_size) in all_resolved.into_iter().zip(sizes) {
        if resolved_size > PACKET_SIZE {
            println!("LARGE FILE: {}", resolved.get_path());
            continue
        }
        if packet_size + resolved_size <= PACKET_SIZE {
            packet.push(resolved);
            packet_size += resolved_size;
        } else {
            packets.push(packet);
            packet = vec![resolved];
            total_size += packet_size;
            packet_size = resolved_size;
        }
    }

    if !packet.is_empty() {
        total_size += packet_size;
        packets.push(packet);
    }

    println!("Total content size: MB {}\n", formatted_content_size(total_size));
    packets
}

// Create progress bar for processing packets.
fn create_progress_bar(bar_size: u64) -> ProgressBar {
    let pb = ProgressBar::new(bar_size);
    pb.set_style(ProgressStyle::default_bar());
    pb.set_message("Indexing files");
    pb
}

// Convert packet of ResolvedFilePaths to packet of References.
// Blocks the current thread while the packet is being processed.
async fn resolve_packet_to_references(packet: Vec<Resolved>) -> Vec<Reference> {
    spawn_blocking( move || {
        let reference_vec: Vec<Reference> = packet
            .par_iter()
            .filter_map(|resolved_path| {
                resolved_path.create_reference()
            })
            .collect();
        reference_vec
    }).await.unwrap()
}

fn formatted_content_size(size: u64) -> String {
    format!("{:.2}", size as f64 / 1024.0 / 1024.0)
}