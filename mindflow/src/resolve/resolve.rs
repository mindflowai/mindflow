use crate::resolve::path_resolver::PathResolver;


pub(crate) async fn resolve(references: &Vec<String>) -> Vec<String> {
    let mut resolved_references = Vec::new();
    for reference in references {
        let resolvers = [PathResolver{}];
        let mut resolved = false;
        for resolver in resolvers.iter() {
            if resolver.should_resolve(reference) {
                resolved = true;
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