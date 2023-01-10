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
            Err(e) => {
                log::debug!("Could not read file: {}. error {:?}", self.path, e);
                return None
            }
        };
        match from_utf8(&text_bytes) {
            Ok(text) => {
                let mut hasher = Sha256::new();
                hasher.update(&text_bytes);
                let file_hash = format!("{:x}", hasher.finalize());
                Some(Reference::new("file".to_string(), file_hash, text.to_string(), self.path.clone()))
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
            Err(e) => {
                log::debug!("Could not read file: {}. Error: {:?}", self.path, e);
                None
            }
        }
    }

    pub fn text_hash(&self) -> Option<String> {
        let text_bytes = match fs::read(self.path.clone()) {
            Ok(bytes) => bytes,
            Err(e) => {
                log::debug!("Could not read file: {}. Error: {:?}", self.path, e);
                return None
            }
        };
        
        // Create a Sha256 hasher
        let mut hasher = Sha256::new();
        hasher.update(text_bytes);

        // Create and return the sha256 hash of the file
        Some(format!("{:x}", hasher.finalize()))
    }
}

// ResolvedFilePath implements the Resolved trait to resolve references in the PathResolved type.
pub struct PathResolver {}

impl PathResolver {
    pub fn extract_files(&self, path: &Path) -> Vec<String> {
        // If the path is a file, return it as the only item in a vector
        if path.is_file() {
            return vec![path.to_string_lossy().to_string()];
        }

        // Check if the path is within a git repository
        if is_within_git_repo(path) {
            return get_git_files(path);
        } 

        // Read all the files and directories in the path, and recursively extract files from directories
        let mut file_paths = Vec::new();
        match fs::read_dir(path) {
            Ok(entries) => {
                for entry in entries {
                    match entry {
                        Ok(entry) => {
                            let path = entry.path();
                            match path.is_dir() {
                                true => {
                                    file_paths.extend(self.extract_files(&path));
                                },
                                false => {
                                    file_paths.push(path.to_string_lossy().to_string());
                                }
                            }
                        },
                        // If the directory could not be read, log the error
                        Err(e) => {
                            log::debug!("Could not read directory: {}. Error: {:?}", path.to_string_lossy(), e);
                        }
                    }
                }
                file_paths
            },
            // If the directory could not be read, log the error
            Err(e) => {
                log::debug!("Could not read directory: {}. Error: {:?}", path.to_string_lossy(), e);
                file_paths
            }
        }
    }

    pub fn should_resolve(&self, path_string: &str) -> bool {
        let path = Path::new(path_string);
        path.is_dir() || path.is_file()
    }

    pub async fn resolve(&self, path: &str) -> Vec<Resolved> {
        // Create a ResolvedPath for each file path and return it as a vec
        self.extract_files(Path::new(path))
            .into_iter()
            .map(|file_path| Resolved::ResolvedFilePath(ResolvedFilePath { path: file_path }))
            .collect()
    }
}
