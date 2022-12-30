use std::env;
use std::fs;
use std::path::Path;
use lazy_static::lazy_static;


pub struct Config {
    api_location: String,
    auth_token: String
}

impl Config {
    pub fn new() -> Config {
        Config {
            api_location: "http://127.0.0.1:5000/api/users".to_string(),
            auth_token: fs::read_to_string(Path::new(&env::var("HOME").unwrap()).join(".mindflow")).expect("Failed to read .mindflow file")
        }
    }

    pub fn get_api_location(&self) -> String {
        self.api_location.clone()
    }

    pub fn get_auth_token(&self) -> String {
        self.auth_token.clone()
    }
}

lazy_static!{
    pub static ref CONFIG: Config = Config::new(); 
}
