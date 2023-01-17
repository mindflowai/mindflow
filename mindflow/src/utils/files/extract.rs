use std::{path::Path, fs};

use super::git::{is_within_git_repo, get_git_files};



pub fn extract_files(path: &Path) -> Vec<String> {
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
                                file_paths.extend(extract_files(&path));
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
