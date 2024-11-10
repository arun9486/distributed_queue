from flask import Flask, request, jsonify
import logging

from queue_repository import QueueRepository



class Driver():
    
  def __init__(self):   
    self.app = Flask(__name__)

    logging.basicConfig(
        filename='/tmp/application.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    self.queue_repo = QueueRepository()

    # Health check endpoint
    @self.app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    # Create a new queue
    @self.app.route("/create", methods=["POST"])
    def create_queue():
        queue_name = request.json.get("queue_name")
        retention_time = request.json.get("retention_time")

        # logging.info(f"creating queue with name {queue_name} and retention perdiod {retention_time}")
        # id = self.queue_repo.create(queue_name, retention_time)
        # logging.info(f"queue for {queue_name} created with id {str(id)}")

        return jsonify({"name": queue_name, "id": str(id)}), 201
 
  def start_server(self):
    self.app.run(host="0.0.0.0", port=8080)
      

driver = Driver()
driver.start_server()