use crate::resolve::path_resolver::PathResolver;


pub(crate) async fn resolve(references: &Vec<String>, index: bool) -> Vec<String> {
    let mut resolved_references = Vec::new();
    for reference in references {
        let resolvers = [PathResolver{}];
        let mut resolved = false;
        for resolver in resolvers.iter() {
            if resolver.should_resolve(reference) {
                resolved = true;
                if index {
                    let processed_hashes = resolver.index_and_resolve(reference).await;
                    resolved_references.extend(processed_hashes);
                    continue;
                }
                let processed_hashes = resolver.resolve(reference).await;
                resolved_references.extend(processed_hashes);
            }
        }
        if !resolved {
            println!("Could not resolve reference: {}", reference);
        }
    }
    resolved_references
}