use clap::{Parser};

use crate::resolve::resolve::{resolve};
use crate::utils::generate_index::generate_index;

#[derive(Parser)]
pub(crate) struct Generate {
    #[arg(index = 1)]
    pub(crate) references: Vec<String>,
}

impl Generate {
    pub(crate) async fn execute(&mut self) {
        let resolved = resolve(&self.references).await;
        generate_index(resolved).await;

        println!("Indexing complete");
    }
}
