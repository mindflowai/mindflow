import sys
from typing import List, Tuple, Type, TypeVar, Union
from typing import Optional
import numpy as np

import pinecone  # type: ignore
from mindflow.core.settings import Settings


def return_values_as_dict(values: List[dict]) -> dict:
    return {value["name"]: value["value"] for value in values}


class Pinecone:
    def __init__(self):
        self.got_indexes = False

    def get_index(self, collection: str) -> pinecone.Index:
        if not self.got_indexes:
            settings = Settings()
            if not hasattr(settings.services.pinecone, "api_key"):
                print(
                    "No Pinecone API key found. Please set Pinecone API key with `mf login`."
                )
                sys.exit(1)

            pinecone.init(
                api_key=settings.services.pinecone.api_key,
                environment=settings.services.pinecone.environment,
            )
            if "mindflow" not in pinecone.list_indexes():
                pinecone.create_index("mindflow", dimension=1536)

            self.indexes = {
                "Document": pinecone.Index("mindflow"),
                "DocumentChunk": pinecone.Index("mindflow"),
            }
            self.got_indexes = True
        if collection not in self.indexes:
            raise ValueError(f"Unknown collection: {collection}")

        return self.indexes[collection]


pinecone_db = Pinecone()

T = TypeVar("T", bound="PineconeStore")


class PineconeStore:
    id: str
    embedding: list

    def __init__(self, id: Union[str, dict]):
        if isinstance(id, dict):
            if not "id" in id:
                raise ValueError("id is required")
            for key, value in id.items():
                setattr(self, key, value)
        else:
            self.id = id

    @staticmethod
    def _convert_pinecone_format_to_object_format(object: dict) -> dict:
        return {
            **{"id": object["id"], "embedding": object["values"]},
            **object["metadata"],
        }

    def _convert_object_to_pinecone_format(self) -> Tuple:
        return (
            self.id,
            self.embedding,
            {
                key: value
                for key, value in self.__dict__.items()
                if key not in ["embedding"]
            },
        )

    @classmethod
    async def load(cls: Type[T], object_id: str) -> Optional[T]:
        if not (object := pinecone_db.get_index(cls.__name__).fetch(ids=[object_id])):
            return None
        return cls(cls._convert_pinecone_format_to_object_format(object["matches"][0]))

    @classmethod
    async def load_bulk(cls: Type[T], object_ids: List[str]) -> List[Optional[T]]:
        vectors = pinecone_db.get_index(cls.__name__).fetch(ids=object_ids)["vectors"]
        vector_list: List[Optional[T]] = [
            cls(cls._convert_pinecone_format_to_object_format(vectors[obj_id]))
            if obj_id in vectors
            else None
            for obj_id in object_ids
        ]
        return vector_list

    @classmethod
    async def load_bulk_ignore_missing(cls: Type[T], object_ids: List[str]) -> List[T]:
        vectors = pinecone_db.get_index(cls.__name__).fetch(ids=object_ids)["vectors"]
        vector_list: List[Optional[T]] = [
            cls(cls._convert_pinecone_format_to_object_format(vectors[obj_id]))
            if obj_id in vectors
            else None
            for obj_id in object_ids
        ]
        return list(filter(None, vector_list))

    @classmethod
    async def delete_bulk(cls, object_ids: List[str]):
        pinecone_db.get_index(cls.__name__).delete(ids=object_ids)

    async def save(self):
        pinecone_db.get_index(self.__class__.__name__).upsert(
            vectors=[self._convert_object_to_pinecone_format()]
        )

    @classmethod
    async def save_bulk(cls, objects: List[T]):
        vectors = [object._convert_object_to_pinecone_format() for object in objects]
        pinecone_db.get_index(cls.__name__).upsert(vectors=vectors)

    @classmethod
    async def query(
        cls: Type[T],
        vector: np.ndarray,
        ids: List[str],
        top_k=100,
        include_metadata=True,
    ) -> List[T]:
        results = pinecone_db.get_index(cls.__name__).query(
            vector=vector.tolist(),
            filter={"id": {"$in": ids}},
            top_k=top_k,
            include_metadata=include_metadata,
        )
        return [
            cls(cls._convert_pinecone_format_to_object_format(result))
            for result in results["matches"]
        ]
