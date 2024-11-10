from flask import Flask, request, jsonify
import logging
import json
from queue_repository import QueueRepository
from message_repository import MessageRepository
from infra import DQueue

class Driver():
  def __init__(self):   
    self.app = Flask(__name__)

    logging.basicConfig(
        filename='/tmp/application.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    self.queue_repo = QueueRepository()
    self.message_repo = MessageRepository()

    # Health check endpoint
    @self.app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    # Create a new queue
    @self.app.route("/create", methods=["POST"])
    def create_queue():
        queue_name = request.json.get("queue_name")
        retention_time = request.json.get("retention_time")

        logging.info(f"creating queue with name {queue_name} and retention perdiod {retention_time}")
        id = self.queue_repo.create(queue_name, retention_time)
        logging.info(f"queue for {queue_name} created with id {str(id)}")

        return jsonify({"name": queue_name, "id": str(id)}), 201
      
    @self.app.route("/get", methods=["POST"])
    def get_queue():
        queue_name = request.json.get("queue_name")
        message = DQueue.objects(name=queue_name).first()
        
        if message:
            # Convert the model fields to a dictionary
            message_dict = {column: getattr(message, column) for column in message._columns.keys()}
            return jsonify(message_dict), 200
        else:
            return jsonify({"error": "Queue not found"}), 404
          
    @self.app.route("/send", methods=["POST"])
    def send_message():
        queue_name = request.json.get("queue_name")
        message = request.json.get("message")
        
        self.message_repo.save(queue_name, message)
        return jsonify({"status": "OK"}), 404
        

  def start_server(self):
    self.app.run(host="0.0.0.0", port=8080)
      

driver = Driver()
driver.start_server()