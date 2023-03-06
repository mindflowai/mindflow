from typing import Dict
from typing import Optional

from mindflow.db.db.database import Store
from mindflow.db.db.json import JsonDatabase
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


class DatabaseController:
    def __init__(self, db_config: Optional[Dict] = None):
        self.databases = Databases()


DATABASE_CONTROLLER = DatabaseController()
