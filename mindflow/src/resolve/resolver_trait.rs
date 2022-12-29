use std::{collections::HashMap};
use async_trait::async_trait;

use crate::utils::reference::Reference;

#[async_trait]
pub(crate) trait Resolver {
    fn should_resolve(&self, path_string: &String) -> bool;
    fn resolve(&self, path_string: &String) -> HashMap<String, Reference>;
}
