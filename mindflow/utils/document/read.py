def read_document(doc_path: str, doc_type: str) -> str:
    """
    Read document
    """
    if doc_type == "file":
        with open(doc_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise Exception(f"Document type {doc_type} not supported")
