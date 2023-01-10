use crate::resolve::file_path_resolver::PathResolver;
use crate::utils::reference::Reference;

use super::{file_path_resolver::ResolvedFilePath};

// This code can be improved by using enums to represent the different types of resolvers and resolved types.
pub enum Resolver {
    PathResolver(PathResolver),
}

pub enum Resolved {
    ResolvedFilePath(ResolvedFilePath),
}

impl Resolver {
    pub fn should_resolve(&self, path: &str) -> bool {
        match self {
            Resolver::PathResolver(resolver) => resolver.should_resolve(path)
        }
    }
    pub async fn resolve(&self, path: &str) -> Vec<Resolved> {
        match self {
            Resolver::PathResolver(resolver) => resolver.resolve(path).await
        }
    }
}

impl Resolved {
    pub fn create_reference(&self) -> Option<Reference> {
        match self {
            Resolved::ResolvedFilePath(resolved_file_path) => resolved_file_path.create_reference(),
        }
    }

    pub fn get_path(&self) -> &str {
        match self {
            Resolved::ResolvedFilePath(resolved_file_path) => resolved_file_path.get_path(),
        }
    }

    pub fn size_bytes(&self) -> Option<u64> {
        match self {
            Resolved::ResolvedFilePath(resolved_file_path) => resolved_file_path.size_bytes(),
        }
    }

    pub fn text_hash(&self) -> Option<String> {
        match self {
            Resolved::ResolvedFilePath(resolved_file_path) => resolved_file_path.text_hash(),
        }
    }
}



// If more resolvers are added, the program must handle the returned resolved types using dynamic dispatch.
// Or better, I could use enums to represent the different types of resolvers which would be more efficient.
pub(crate) async fn resolve(references: &Vec<String>) -> Vec<Resolved> {
    let resolvers = [Resolver::PathResolver(PathResolver{})];
    let mut resolved_references: Vec<Resolved> = Vec::new();
    for reference in references {
        let mut resolved = false;
        for resolver in resolvers.iter() {
            if resolver.should_resolve(reference) {
                resolved = true;
                let resolved = resolver.resolve(reference).await;
                resolved_references.extend(resolved);
            }
        }
        if !resolved {
            println!("Could not resolve reference: {}", reference);
        }
    }
    resolved_references
}
