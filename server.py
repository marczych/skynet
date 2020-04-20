#!/usr/bin/env python3

import argparse
import json
import os
import subprocess

import tornado.ioloop
import tornado.web


# Populated during startup.
CONFIG = dict(
    command_directory=None,
    commands=None,
)


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


def make_app():
    return tornado.web.Application([
        (r"/api/send", SendHandler),
    ])


def configure(command_directory: str) -> None:
    CONFIG["command_directory"] = command_directory
    CONFIG["commands"] = set(os.listdir(command_directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command_directory")
    args = parser.parse_args()

    configure(args.command_directory)

    print(f"Running with config: {CONFIG}")

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
