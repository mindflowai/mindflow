// Sends a basic completion prompt to the Mindflow server to get a response from GPT model.

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
            prompt: prompt,
            auth: CONFIG.get_auth_token()
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct PromptResponse {
    pub(crate) text: String,
}

pub(crate) async fn request_prompt(client:&Client, prompt: String) -> Result<PromptResponse, reqwest::Error> {
    let prompt_request: PromptRequest = PromptRequest::new(prompt);
    let res = client
        .post(&format!("{}/prompt", CONFIG.get_api_location()))
        .json(&prompt_request)
        .send()
        .await?
        .json::<PromptResponse>()
        .await?;
    
    Ok(res)
}