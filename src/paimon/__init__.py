import os
import http

from flask import Flask, request

app = Flask(__name__)
app.config.from_object("paimon.default_settings")
if "PAIMON_SETTINGS" in os.environ:
    app.config.from_envvar("PAIMON_SETTINGS")


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    return ("", http.HTTPStatus.NO_CONTENT)
