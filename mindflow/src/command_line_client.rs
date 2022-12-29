use clap::Parser;

use crate::commands::query::Query;
use crate::commands::auth::Auth;
use crate::commands::diff::Diff;
use crate::commands::ask::Ask;


#[derive(Parser)]
#[command(author, version, about, long_about = None)]
pub(crate) enum CommandLineClient {
    Query(Query),
    Auth(Auth),
    Diff(Diff),
    Ask(Ask),
}

impl CommandLineClient {
    pub(crate) async fn execute(&mut self) {
        match self {
            CommandLineClient::Query(cmd) => cmd.execute().await,
            CommandLineClient::Auth(cmd) => cmd.execute().await,
            CommandLineClient::Diff(cmd) => cmd.execute().await,
            CommandLineClient::Ask(cmd) => cmd.execute().await,
        };
    }
}