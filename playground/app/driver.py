from flask import Flask, request, jsonify

app = Flask(__name__)

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Create a new queue
@app.route("/create", methods=["POST"])
def create_queue():
    queue_name = request.json.get("queue_name")
    retention_time = request.json.get("retention_time")
    
    # TODO change response
    return jsonify({"message": "Queue created"}), 201
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)