use crate::utils::reference::Reference;

pub(crate) trait Resolved {
    fn create_reference(&self) -> Option<Reference>;
    fn r#type(&self) -> String;
    fn size_bytes(&self) -> Option<u64>;
    fn text_hash(&self) -> Option<String>;
}
