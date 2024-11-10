from xmlrpc.server import SimpleXMLRPCServer
import logging

def store_message(queue_name, message):
  print("Not implemented")

def delete_message(queue_name, message):
  print("Not implemented")

# Initialize the server on localhost and port 8000
server = SimpleXMLRPCServer(("localhost", 8000))
logging.info("RPC Server is running on port 8000...")

# Register functions to be accessible via RPC
server.register_function(store_message, "store_message")
server.register_function(delete_message, "delete_message")

try:
    server.serve_forever()
except KeyboardInterrupt:
    logging.info("Server stopped.")