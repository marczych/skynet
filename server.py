#!/usr/bin/env python3

import json
import subprocess

import tornado.ioloop
import tornado.web


class SendHandler(tornado.web.RequestHandler):
    def post(self):
        command = json.loads(self.request.body)["command"]

        if command not in ("volup", "voldown"):
            self.set_status(400)
            self.write(dict(error=f"Unknown command: {command}"))
            return

        subprocess.check_call(
            [
                "ir-ctl",
                "--device",
                "/dev/lirc0",
                "--send",
                command,
            ],
        )

        self.write(dict(success=True, message=f"Ran command: {command}"))


def make_app():
    return tornado.web.Application([
        (r"/api/send", SendHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
