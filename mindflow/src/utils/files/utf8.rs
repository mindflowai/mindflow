use simdutf8::basic::from_utf8;

// Take a file path and read the contents byte, by byte, if the file is valid utf8, return false, otherwise return true
pub fn is_valid_utf8(path: &str) -> bool {
    let text_bytes = match std::fs::read(path) {
        Ok(bytes) => bytes,
        Err(e) => {
            log::debug!("Could not read file: {}. error {:?}", path, e);
            return false
        }
    };
    match from_utf8(&text_bytes) {
        Ok(_text) => true,
        Err(_e) => false
    }
}