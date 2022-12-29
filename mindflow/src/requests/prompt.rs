use serde::{Deserialize, Serialize};
use reqwest::{Client};

use crate::utils::config::API_LOCATION;

#[derive(Serialize)]
pub(crate) struct PromptRequest {
    pub(crate) prompt: String,
}

#[derive(Deserialize)]
pub(crate) struct PromptResponse {
    pub(crate) text: String,
}

pub(crate) async fn request_prompt(client:&Client, prompt: String) -> Result<PromptResponse, reqwest::Error> {
    let res = client
        .post(&format!("{}/prompt", API_LOCATION))
        .json(&PromptRequest { prompt })
        .send()
        .await?
        .json::<PromptResponse>()
        .await?;
    
    Ok(res)
}