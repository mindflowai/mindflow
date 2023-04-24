from typing import List, Tuple
from typing import Optional
import numpy as np

import pinecone  # type: ignore
from mindflow.db.db.database import Database
from mindflow.settings import Settings


def return_values_as_dict(values: List[dict]) -> dict:
    return {value["name"]: value["value"] for value in values}


class PineconeDatabase(Database):
    def __init__(self):
        self.got_indexes = False

    def _get_index(self, collection: str) -> pinecone.Index:
        if not self.got_indexes:
            settings = Settings()
            pinecone.init(
                api_key=settings.services.pinecone.api_key,
                environment=settings.services.pinecone.environment,
            )
            if "mindflow" not in pinecone.list_indexes():
                print("Creating Pinecone index...")
                pinecone.create_index("mindflow", dimension=1536)

            self.indexes = {
                "document": pinecone.Index("mindflow"),
                "document_chunk": pinecone.Index("mindflow"),
            }
            self.got_indexes = True
        if collection not in self.indexes:
            raise ValueError(f"Unknown collection: {collection}")

        return self.indexes[collection]

    def _convert_pinecone_return(self, object: dict) -> dict:
        return {
            **{"id": object["id"], "embedding": object["values"]},
            **object["metadata"],
        }

    def _convert_object_to_pinecone(self, object: dict) -> Tuple:
        return (
            object["id"],
            object["embedding"],
            {key: value for key, value in object.items() if key not in ["embedding"]},
        )

    def load(self, collection: str, object_id: str) -> Optional[dict]:
        index = self._get_index(collection)
        object = index.fetch(ids=[object_id])
        if not object:
            return {}

        return self._convert_pinecone_return(object["matches"][0])

    def load_bulk(self, collection: str, object_ids: List[str]) -> List[Optional[dict]]:
        index = self._get_index(collection)
        vectors = index.fetch(ids=object_ids)["vectors"]

        vector_list: List[Optional[dict]] = [None] * len(object_ids)

        for object_index in range(len(vector_list)):
            obj_id = object_ids[object_index]
            if obj_id in vectors:
                vector_list[object_index] = self._convert_pinecone_return(
                    vectors[obj_id]
                )

        return vector_list

    def delete_bulk(self, collection: str, object_ids: List[str]):
        index = self._get_index(collection)
        index.delete(ids=object_ids)

    def save(self, collection: str, value: dict):
        index = self._get_index(collection)
        index.upsert(vectors=[self._convert_object_to_pinecone(value)])

    def save_bulk(self, collection: str, values: List[dict]):
        index = self._get_index(collection)
        vectors = [self._convert_object_to_pinecone(value) for value in values]
        index.upsert(vectors=vectors)

    def query(
        self,
        collection: str,
        vector: np.ndarray,
        ids: List[str],
        top_k=100,
        include_metadata=True,
    ) -> List[dict]:
        index = self._get_index(collection)
        results = index.query(
            vector=vector.tolist(),
            filter={"id": {"$in": ids}},
            top_k=top_k,
            include_metadata=include_metadata,
        )
        return [self._convert_pinecone_return(result) for result in results["matches"]]


PINECONE_DATABASE = PineconeDatabase()
