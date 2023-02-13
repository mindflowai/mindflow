# Generic accessors

import sys


from mindflow.db.locations.json import JsonDatabase
from mindflow.db.locations.neo4j import (
    Neo4jDatabase,
)
from mindflow.db.locations.static import Static
from mindflow.db.static_definition import ObjectStoreType


class Database:
    def __init__(self):
        self.json = JsonDatabase()
        self.static = Static()

    def set_db_config(self, db_config: dict):
        self.db_config = db_config

    @property
    def graph_database(self):
        database = self.db_config.get("graph_database", None)
        if database:
            neo4j_config = database.get(ObjectStoreType.NEO4J.value, None)
            if neo4j_config:
                return Neo4jDatabase(neo4j_config)
        print(
            "Invalid or missing Neo4j configuration. Please check your configuration file."
        )
        sys.exit(1)

    def save_json(self):
        self.json.save()


DATABASE = Database()
