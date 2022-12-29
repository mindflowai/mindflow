use std::collections::{HashMap};
use std::fs;
use std::path::Path;
use std::str::from_utf8;
use rayon::prelude::*;

use reqwest::Client;
use sha2::{Digest, Sha256};
use tokio::task::spawn_blocking;

use crate::requests::unindexed_references::{request_unindexed_references};
use crate::requests::index_references::{request_index_references};
use crate::utils::git::{get_git_files, is_within_git_repo};
use crate::utils::reference::Reference;


const PACKET_SIZE: u64 = 2 * 1024 * 1024; // 2 MB

pub(crate) struct PathResolver {}

impl PathResolver {
    pub fn extract_files(&self, path: &Path) -> Vec<String> {
        if path.is_dir() {
            if is_within_git_repo(path) {
                return get_git_files(path)
            } else {
                panic!("Path is not within a git repository")
            }
        } else {
            vec![path.to_string_lossy().to_string()] 
        }
    }
}

impl PathResolver {
    pub fn should_resolve(&self, path_string: &String) -> bool {
        let path = Path::new(path_string);
        path.is_dir() || path.is_file()
    }

    pub async fn resolve(&self, path: &str) -> Vec<String> {
        let client = Client::new();
        let mut processed_hashes: Vec<String> = Vec::new();

        let file_paths = self.extract_files(Path::new(path));
        
        let sizes: Vec<u64> = file_paths
            .par_iter()
            .map(|file_path| {
                fs::metadata(file_path).unwrap().len()
            })
            .collect();

        let mut packets: Vec<Vec<String>> = Vec::new();
        let mut packet: Vec<String> = Vec::new();

        let mut size: u64 = 0;
        let mut total_size = 0;

        for (file_path, file_size) in file_paths.iter().zip(sizes) {
            if size + file_size <= PACKET_SIZE {
                packet.push(file_path.to_owned());
                size += file_size;
            } else {
                packets.push(packet);
                packet = vec![file_path.to_owned()];
                total_size += size;
                size = file_size;
            }
        }

        if !packet.is_empty() {
            total_size += size;
            packets.push(packet);
        }

        for packet in packets {
            let result = spawn_blocking( move || {
                let reference_vec: Vec<Reference> = packet
                    .par_iter()
                    .filter_map(|file_path| {
                        let file_bytes = fs::read(file_path.clone()).unwrap();
                        match from_utf8(&file_bytes) {
                            Ok(text) => {
                                let mut hasher = Sha256::new();
                                hasher.update(&file_bytes);
                                let file_hash = format!("{:x}", hasher.finalize());
                                let reference = Reference::new("file".to_string(), file_hash, text.to_string(), file_bytes.len(), file_path.to_string());
                                Some(reference)
                            },
                            Err(e) => {
                                dbg!("Could not convert bytes to utf8: {}", file_path);
                                None
                            }
                        }
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
                Err(_) => {
                    println!("Error: Could not get unindexed hashes");
                    Vec::new()
                }
            };
            request_index_references(&client, data_map, unindexed_hashes).await;

            processed_hashes.extend(hashes);
        }
        processed_hashes
    }
}
