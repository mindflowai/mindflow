// Sends a basic completion prompt to the Mindflow server to get a response from GPT model.
use std::process;

use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::utils::config::{CONFIG};

#[derive(Serialize)]
pub(crate) struct PromptRequest {
    pub(crate) prompt: String,
    pub(crate) auth: String
}

impl PromptRequest {
    pub fn new(prompt: String) -> PromptRequest {
        PromptRequest {
            prompt,
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct PromptResponse {
    pub(crate) text: String,
}

// Sends a basic completion prompt to the Mindflow server to get a response from GPT model.
pub(crate) async fn request_prompt(client: &Client, prompt: String) -> PromptResponse {
    let prompt_request: PromptRequest = PromptRequest::new(prompt);
    let res = client
        .post(&format!("{}/prompt", CONFIG.get_api_location()))
        .json(&prompt_request)
        .send()
        .await;

    // match server response
    match res {
        Ok(res) => {
            // match status code
            match res.status().as_u16() {
                400 => {
                    println!("Invalid authorization token.");
                    process::exit(1);
                }
                _ => {
                    match res.json().await {
                        Ok(prompt_response) => prompt_response,
                        Err(e) => {
                            println!("Error: Could not get prompt response: {}", e);
                            process::exit(1);
                        }
                    }
                }
            }
        },
        Err(e) => {
            println!("Error: Could not get prompt response: {}", e);
            process::exit(1);
        }
    }
}
