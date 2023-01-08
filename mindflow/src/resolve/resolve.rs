use crate::resolve::file_path_resolver::PathResolver;

use super::{file_path_resolver::ResolvedFilePath};

// If more resolvers are added, the program must handle the returned resolved types using dynamic dispatch.
// Or better, I could use enums to represent the different types of resolvers which would be more efficient.
pub(crate) async fn resolve(references: &Vec<String>) -> Vec<ResolvedFilePath> {
    let mut resolved_references: Vec<ResolvedFilePath> = Vec::new();
    for reference in references {
        let resolvers = [PathResolver{}];
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
