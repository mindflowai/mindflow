from flask import Flask
from flask import request


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

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

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

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

        @self.app.route("/diff", methods=["POST"])
        def diff_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["git_diff_args", "return_prompt", "skip_clipboard"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

        @self.app.route("/inspect", methods=["POST"])
        def inspect_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

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

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

        @self.app.route("/refresh", methods=["POST"])
        def refresh_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths", "force"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

        @self.app.route("/index", methods=["POST"])
        def index_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})


api = API()
app = api.app
app.run()
