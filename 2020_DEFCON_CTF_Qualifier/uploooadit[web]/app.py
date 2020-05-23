import os
import re

from flask import Flask, abort, request

import store

GUID_RE = re.compile(
    r"\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z"
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512
filestore = store.S3Store()

# Uncomment the following line for simpler local testing of this service
# filestore = store.LocalStore()


@app.route("/files/", methods=["POST"])
def add_file():
    if request.headers.get("Content-Type") != "text/plain":
        abort(422)

    guid = request.headers.get("X-guid", "")
    if not GUID_RE.match(guid):
        abort(422)

    filestore.save(guid, request.data)
    return "", 201


@app.route("/files/<guid>", methods=["GET"])
def get_file(guid):
    if not GUID_RE.match(guid):
        abort(422)

    try:
        return filestore.read(guid), {"Content-Type": "text/plain"}
    except store.NotFound:
        abort(404)


@app.route("/", methods=["GET"])
def root():
    return "", 204
