use clap::{Parser};

use crate::command_helpers::auth::set_token;

#[derive(Parser)]
pub(crate) struct Auth {
    pub(crate) auth_key: Option<String>,
}

impl Auth {
    pub(crate) async fn execute(&mut self) {
        set_token(self.auth_key.clone()).await;
    }
}
