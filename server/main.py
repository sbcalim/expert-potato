import logging

from flask import Flask, jsonify
from server import logger

app = Flask(__name__)

@app.route("/")
def index():
    logging.debug("Request is sending to the root url.")
    return jsonify(message="Server is running!", app="Expert Potato")

@app.route("/health")
def health_check():
    logger.info("Checking health.")
    return jsonify(
        service="Expert Potato",
        version="0.0.1",
    ), 200

def start_server():
    logging.info("Starting server on port 5000.")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_server()