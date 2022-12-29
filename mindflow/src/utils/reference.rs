use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
#[derive(Clone)]
#[derive(Debug)]
pub(crate) struct Reference {
    pub(crate) r#type: String,
    pub(crate) hash: String,
    pub(crate) text: String,
    pub(crate) size: usize,
    pub(crate) path: String,
}

impl Reference {
    pub fn new(r#type: String, hash: String, text: String, size: usize, path: String) -> Reference {
        Reference {
            r#type,
            hash,
            text,
            size,
            path,
        }
    }

    pub fn get_text(&self) -> &String {
        &self.text
    }

    pub fn get_type(&self) -> &String {
        &self.r#type
    }

    pub fn get_path(&self) -> &String {
        &self.path
    }
}
