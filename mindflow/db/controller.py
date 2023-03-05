from typing import Dict, Optional

from mindflow.db.db.database import Database, Store
from mindflow.db.db.json import JsonDatabase
from mindflow.db.db.neo4j import Neo4jDatabase
from mindflow.db.db.static import Static


class Databases:
    def __init__(self):
        self.databases = {}

    @property
    def static(self) -> Static:
        if Store.STATIC not in self.databases:
            self.databases[Store.STATIC] = Static()
        return self.databases[Store.STATIC]
    
    @property
    def json(self) -> JsonDatabase:
        if Store.JSON not in self.databases:
            self.databases[Store.JSON] = JsonDatabase()
        return self.databases[Store.JSON]
    
    @property
    def neo4j(self) -> Neo4jDatabase:
        if Store.NEO4J not in self.databases:
            self.databases[Store.NEO4J] = Neo4jDatabase()
        return self.databases[Store.NEO4J]


class DatabaseController:
    def __init__(self, db_config: Optional[Dict] = None):
        self.databases = Databases()

DATABASE_CONTROLLER = DatabaseController()