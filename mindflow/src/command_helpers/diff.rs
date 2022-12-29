use std::process::Command;
use crate::utils::prompts::GIT_DIFF_PROMPT_PREFIX;

pub async fn generate_diff_prompt(diffargs: &Vec<String>) -> String {
    let command = ["git", "diff"]
        .iter()
        .map(|s| s.to_string())
        .chain(diffargs.iter().map(|s| s.to_string()))
        .collect::<Vec<_>>();

    let diff_result = Command::new(&command[0])
        .args(&command[1..])
        .output()
        .expect("failed to execute process");
    
        

    format!("{}\n\n{}", GIT_DIFF_PROMPT_PREFIX, String::from_utf8_lossy(&diff_result.stdout))
}