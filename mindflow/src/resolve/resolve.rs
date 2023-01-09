use crate::resolve::file_path_resolver::PathResolver;
use crate::utils::reference::Reference;

use super::{file_path_resolver::ResolvedFilePath};

// This code can be improved by using enums to represent the different types of resolvers and resolved types.

// Resolved is a trait that all resolved references must implement.
pub(crate) trait Resolved {
    fn create_reference(&self) -> Option<Reference>;
    fn r#type(&self) -> String;
    fn size_bytes(&self) -> Option<u64>;
    fn text_hash(&self) -> Option<String>;
}

// If more resolvers are added, the program must handle the returned resolved types using dynamic dispatch.
// Or better, I could use enums to represent the different types of resolvers which would be more efficient.
pub(crate) async fn resolve(references: &Vec<String>) -> Vec<ResolvedFilePath> {
    let resolvers = [PathResolver{}];
    let mut resolved_references: Vec<ResolvedFilePath> = Vec::new();
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

// // Enum to represent the different types of resolvers.
// enum Resolver {
//     Path(PathResolver),
//     // Add other resolver types here
// }

// // Implement the `should_resolve` and `resolve` methods for each variant of the `Resolver` enum.
// impl Resolver {
//     fn should_resolve(&self, reference: &String) -> bool {
//         match self {
//             Resolver::Path(resolver) => resolver.should_resolve(reference),
//             // Add other resolver types here
//         }
//     }

//     async fn resolve(&self, reference: &String) -> Vec<ResolvedFilePath> {
//         match self {
//             Resolver::Path(resolver) => resolver.resolve(reference).await,
//             // Add other resolver types here
//         }
//     }
// }
