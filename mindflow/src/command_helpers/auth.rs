use std::env;
use std::fs;
use std::path::Path;
use dialoguer::{theme::ColorfulTheme ,Input};

pub async fn set_token(auth_key: Option<String>) {
    let token = match auth_key {
        Some(token) => {
            token
        } None => {
            let input: String = Input::with_theme(&ColorfulTheme::default())
                .with_prompt("Authorization token: ")
                .interact_text()
                .unwrap();
            input
        }
    };

    let home_dir = env::var("HOME").unwrap();
    let path = Path::new(&home_dir).join(".mindflow");

    let result = fs::write(path, token).map_err(|e| e.to_string());

    match result {
        Ok(_) => {
            println!("Successfully authorized with token");
        }
        Err(e) => {
            println!("Error: {}", e);
            std::process::exit(1);
        }
    }
}