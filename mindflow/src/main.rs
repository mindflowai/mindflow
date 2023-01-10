pub mod utils;
pub mod resolve_handling;
pub mod commands;
pub mod requests;
pub mod command_helpers;
pub mod command_line_client;

use clap::Parser;

use crate::command_line_client::CommandLineClient;

#[tokio::main]
async fn main() {
    let mut client: CommandLineClient = CommandLineClient::parse();
    client.execute().await;
}
