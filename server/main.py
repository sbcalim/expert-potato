from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(message="Server is running!", app="Expert Potato")

@app.route("/health")
def health_check():
    return jsonify(
        service="Expert Potato",
        version="0.0.1",
    ), 200

def start_server():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_server()