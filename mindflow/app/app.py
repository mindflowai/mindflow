from flask import Flask, request

from mindflow.input import Arguments, Command, DBConfig
from mindflow.state import STATE, ConfiguredModel, ConfiguredService

from mindflow.commands.ask import ask
# from mindflow.commands.config import config
from mindflow.commands.delete import delete
from mindflow.commands.diff import diff
from mindflow.commands.index import index
from mindflow.commands.inspect import inspect
from mindflow.commands.query import query


def trim_json(data: dict, keys: list) -> dict:
    return {key: data[key] for key in keys if key in data}


class API:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route("/ask", methods=["POST"])
        def ask_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["query", "return_prompt", "skip_clipboard"]
            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.ASK.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.ASK.value

            ask()

        @self.app.route("/config", methods=["POST"])
        def config_route():
            # Your implementation for Command.CONFIG
            pass

        @self.app.route("/delete", methods=["POST"])
        def delete_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]

            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.DELETE.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.DELETE.value

            delete()

        @self.app.route("/diff", methods=["POST"])
        def diff_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["git_diff_args", "return_prompt", "skip_clipboard"]
            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.DIFF.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.DIFF.value

            diff()

        @self.app.route("/inspect", methods=["POST"])
        def inspect_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]
            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.INDEX.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            inspect()

        @self.app.route("/query", methods=["POST"])
        def query_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = [
                "document_paths",
                "index",
                "query",
                "return_prompt",
                "skip_clipboard",
            ]
            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.QUERY.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.QUERY.value

            query()

        @self.app.route("/refresh", methods=["POST"])
        def refresh_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths", "force"]
            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.REFRESH.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.REFRESH.value

            index()

        @self.app.route("/index", methods=["POST"])
        def index_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]
            arguments = trim_json(arguments, keys_to_keep)

            db_config = params.get("db_config", None)
            path = params.get("path", None)

            STATE.db_config = DBConfig(db_config, path)
            STATE.configured_service = ConfiguredService(STATE.db_config)
            STATE.configured_model = ConfiguredModel(
                Command.INDEX.value, STATE.configured_service, STATE.db_config
            )
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            index()


api = API()
app = api.app
app.run()