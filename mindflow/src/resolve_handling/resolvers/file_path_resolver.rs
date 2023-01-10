// Contains the implementation of the PathResolver struct and the ResolvedFilePath struct.
// ResolvedFilePath:
//    - Implements the Resolved trait.
// PathResolver:
//    - Implements the Resolver trait.

use std::{fs};
use std::path::Path;
use std::str::from_utf8;

use sha2::{Digest, Sha256};

use crate::resolve_handling::resolve::Resolved;
use crate::utils::{git::{get_git_files, is_within_git_repo}, reference::Reference};

pub struct ResolvedFilePath {
    pub path: String,
}

// ResolvedFilePath implements the Resolved trait create a reference and extract other data about the file. 
impl ResolvedFilePath {
    pub fn create_reference(&self) -> Option<Reference> {
        let text_bytes = match fs::read(self.path.clone()) {
            Ok(bytes) => bytes,
            Err(_e) => {
                log::debug!("Could not read file: {}", self.path);
                return None
            }
        };
        match from_utf8(&text_bytes) {
            Ok(text) => {
                let mut hasher = Sha256::new();
                hasher.update(&text_bytes);
                let file_hash = format!("{:x}", hasher.finalize());
                let reference = Reference::new("file".to_string(), file_hash, text.to_string(), text_bytes.len(), self.path.clone());
                Some(reference)
            },
            Err(_e) => {
                log::debug!("Could not convert bytes to utf8: {}", self.path);
                None
            }
        }
    }

    pub fn get_path(&self) -> &str {
        &self.path
    }

    pub fn size_bytes(&self) -> Option<u64> {
        match fs::metadata(self.path.clone()) {
            Ok(meta_data) => Some(meta_data.len()),
            Err(_e) => {
                log::debug!("Could not read file: {}", self.path);
                None
            }
        }
    }

    pub fn text_hash(&self) -> Option<String> {
        let text_bytes = match fs::read(self.path.clone()) {
            Ok(bytes) => bytes,
            Err(_e) => {
                log::debug!("Could not read file: {}", self.path);
                return None
            }
        };
        let mut hasher = Sha256::new();
        hasher.update(text_bytes);
        Some(format!("{:x}", hasher.finalize()))
    }
}

// ResolvedFilePath implements the Resolved trait to resolve references in the PathResolved type.
pub struct PathResolver {}

impl PathResolver {
    pub fn extract_files(&self, path: &Path) -> Vec<String> {
        // println!("Extracting files from: {}", path.to_string_lossy());
        if path.is_dir() {
            if is_within_git_repo(path) {
                get_git_files(path)
            } 
            else {
                let mut file_paths: Vec<String> = Vec::new();
                match fs::read_dir(path) {
                    Ok(entries) => {
                        entries.for_each(|entry| {
                            match entry {
                                Ok(entry) => {
                                    let path = entry.path();
                                    if path.is_dir() {
                                        file_paths.extend(self.extract_files(&path));
                                    } else {
                                        file_paths.push(path.to_string_lossy().to_string());
                                    }
                                },
                                Err(_e) => {
                                    log::debug!("Could not read directory: {}", path.to_string_lossy());
                                }
                            }
                        });
                        file_paths
                    },
                    Err(_e) => {
                        log::debug!("Could not read directory: {}", path.to_string_lossy());
                        file_paths
                    }
                }
            }
        } else {
            vec![path.to_string_lossy().to_string()] 
        }
    }

    pub fn should_resolve(&self, path_string: &str) -> bool {
        let path = Path::new(path_string);
        path.is_dir() || path.is_file()
    }

    pub async fn resolve(&self, path: &str) -> Vec<Resolved> {
        let file_paths = self.extract_files(Path::new(path));
        // Create a ResolvedPath for each file path and return it as a vec
        let resolved_paths: Vec<Resolved> = file_paths.iter().map(|file_path| Resolved::ResolvedFilePath(ResolvedFilePath { path: file_path.to_string() })).collect();
        resolved_paths
    }
}
