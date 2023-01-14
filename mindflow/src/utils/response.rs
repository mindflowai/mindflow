use clipboard::{ClipboardContext, ClipboardProvider};

pub fn handle_response_text(text: String, skip_clipboard: bool) {
    if !skip_clipboard {
        let mut ctx: ClipboardContext = ClipboardProvider::new().unwrap_or_else(|e| {
            panic!("Failed to create clipboard context: {}", e);
        });
        ctx.set_contents(text).unwrap_or_else(|e| {
            panic!("Failed to copy to clipboard: {}", e);
        });
        println!("Response copied to clipboard!!!");
        return
    }
    println!("{}", text);
}