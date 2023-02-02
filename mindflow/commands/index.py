"""
`generate` command
"""
from asyncio import Future
from typing import List
from concurrent.futures import ThreadPoolExecutor

from alive_progress import alive_bar

from mindflow.state import STATE
from mindflow.db.db import set_object
from mindflow.db.objects.document import Document
from mindflow.utils.document.read import read_document
from mindflow.index.search_tree import create_text_search_tree


def index():
    """
    This function is used to generate an index and/or embeddings for files
    """
    if not STATE.indexable_document_references:
        print("No documents to index")
        return

    total_size = sum(
        [
            document_reference.size
            for document_reference in STATE.indexable_document_references
        ]
    )
    print(f"Total content size: MB {total_size / 1024 / 1024:.2f}")
    # build search trees in parallel
    with alive_bar(
        len(STATE.indexable_document_references), bar="blocks", spinner="twirls"
    ) as progress_bar:

        with ThreadPoolExecutor(max_workers=25) as executor:
            search_tree_futures: List[Future[dict]] = [
                executor.submit(
                    create_text_search_tree,
                    read_document(
                        document_reference.path, document_reference.document_type
                    ),
                )
                for document_reference in STATE.indexable_document_references
            ]

            for search_tree_future, document_reference in zip(
                search_tree_futures, STATE.indexable_document_references
            ):
                document = Document(document_reference.__dict__)
                document.search_tree = search_tree_future.result()
                set_object(
                    document_reference.path, document.__dict__, STATE.db_config.document
                )
                del document_reference, search_tree_future
                progress_bar()
