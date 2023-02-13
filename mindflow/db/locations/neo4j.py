import sys
from typing import List, Optional

from neo4j import GraphDatabase


class Neo4jDatabase:
    def __init__(self, config: dict):
        self.config = config

    @property
    def driver(self):
        uri = self.config.get("uri", None)
        if not uri:
            print("No uri provided for Neo4j")
            sys.exit(1)
        auth = self.config.get("auth", None)
        if not auth:
            print("No auth provided for Neo4j")
            sys.exit(1)

        user = auth.get("user", None)
        password = auth.get("password", None)
        if not user or not password:
            print("No user or password provided for Neo4j")
            sys.exit(1)

        return GraphDatabase.driver(uri, auth=(user, password))

    @property
    def session(self):
        return self.driver.session()

    def retrieve_object(self, collection: str, object_id: str) -> Optional[dict]:
        result = self.session.run(
            """
            MATCH (d:{collection}}) WHERE d.id = {object_id}
            RETURN d
        """,
            {"collection": collection, "object_id": object_id},
        )

        return dict(result.single()["d"].items())

    def retrieve_object_bulk(
        self, collection: str, object_ids: List[str]
    ) -> Optional[List[dict]]:
        result = self.session.run(
            """
            UNWIND {object_ids} AS id
            MATCH (d:{collection}) WHERE d.id = id
            RETURN d
        """,
            {"collection": collection, "object_ids": object_ids},
        )

        return [dict(record["d"].items()) for record in result]

    ### Delete objects from json from ID list and overwrite the file
    def delete_object_bulk(self, collection: str, object_ids: List[str]):
        return self.session.run(
            """
            UNWIND {object_ids} AS id
            MATCH (d:{collection}) WHERE d.id = id
            DELETE d
        """,
            {"collection": collection, "object_ids": object_ids},
        )

    def set_object(self, collection: str, value: dict):
        return self.session.run(
            """
            CREATE (d:{collection} {params})
        """,
            {"collection": collection, "params": value},
        )
