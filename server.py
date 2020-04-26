#!/usr/bin/env python3

import argparse
import json
import os
import subprocess

import tornado.ioloop
import tornado.web


# Populated during startup.
CONFIG = dict(command_directory=None, commands=None)


class SendHandler(tornado.web.RequestHandler):
    def post(self):
        command = json.loads(self.request.body)["command"]

        if command not in CONFIG["commands"]:
            self.set_status(400)
            self.write(dict(error=f"Unknown command: {command}"))
            return

        subprocess.check_call(
            [
                "ir-ctl",
                "--device",
                "/dev/lirc0",
                "--send",
                os.path.join(CONFIG["command_directory"], command),
            ],
        )

        self.write(dict(success=True, message=f"Ran command: {command}"))


def make_app(static_dir: str, debug: bool):
    return tornado.web.Application(
        [
            (r"/api/command", SendHandler),
            (
                r"/()",
                tornado.web.StaticFileHandler,
                {"path": os.path.join(static_dir, "index.html")},
            ),
        ],
        static_path=static_dir,
        debug=debug,
    )


def configure(command_directory: str) -> None:
    CONFIG["command_directory"] = command_directory
    CONFIG["commands"] = set(os.listdir(command_directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command_directory")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--debug", action="store_true", default=False)
    args = parser.parse_args()

    configure(args.command_directory)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    port = args.port

    print(f"Running at {app_dir} on port {port} with config: {CONFIG}")

    app = make_app(static_dir=os.path.join(app_dir, "static"), debug=args.debug)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
