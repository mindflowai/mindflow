// Sends a basic completion prompt to the Mindflow server to get a response from GPT model.
use std::process;

use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::utils::config::{CONFIG};

use super::status::http_status::HttpStatus;

#[derive(Serialize)]
pub(crate) struct PromptRequest {
    pub(crate) prompt: String,
    pub(crate) return_prompt: bool,
    pub(crate) auth: String
}

impl PromptRequest {
    pub fn new(prompt: String, return_prompt: bool) -> PromptRequest {
        PromptRequest {
            prompt,
            return_prompt,
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct PromptResponse {
    pub(crate) text: String,
}

// Sends a basic completion prompt to the Mindflow server to get a response from GPT model.
pub(crate) async fn request_prompt(client: &Client, prompt: String, return_prompt: bool) -> PromptResponse {
    let prompt_request: PromptRequest = PromptRequest::new(prompt, return_prompt);
    let res = match client
        .post(&format!("{}/prompt", CONFIG.get_api_location()))
        .json(&prompt_request)
        .send()
        .await {
            Ok(res) => res,
            Err(e) => {
                println!("Error: Could not send prompt request: {}", e);
                process::exit(1);
            }
        };
    
    // match status code
    let status = match res.status().as_u16() {
        200 => HttpStatus::Ok,
        400 => HttpStatus::BadRequest,
        401 => HttpStatus::Unauthorized,
        _   => HttpStatus::InternalServerError
    };

    // match response
    match status {
        HttpStatus::Ok => {
            match res.json().await {
                Ok(prompt_response) => prompt_response,
                Err(e) => {
                    println!("Error: Could not get prompt response: {}", e);
                    process::exit(1);
                }
            }
        }
        HttpStatus::BadRequest => {
            println!("Error: Bad Request.");
            process::exit(1);
        }
        HttpStatus::Unauthorized => {
            println!("Invalid authorization token.");
            process::exit(1);
        }
        HttpStatus::InternalServerError => {
            println!("Error: Could not index references.");
            process::exit(1);
        }
    }
}
