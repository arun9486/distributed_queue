from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
import uuid
from utils import KEYSPACE
from infra import DQueue
import logging
import os
from datetime import datetime
import threading
import time
from utils import list_table_names
from infra import DQueue
from infra import Message
from datetime import date
from pathlib import Path


class MessageRepository():
  def __init__(self):
    self.raw_file_path_prefix = "/home/arun-linux/cassandra/raw_message/"
    thread = threading.Thread(target=self.scan_messages)
    thread.start()
    
  def scan_messages(self):
    while True:
      queues = DQueue.objects.all()
      for queue in queues:
        if "CREATED" != queue.state:
          continue

        logging.info(f"Queue {queue.name} is active. Scanning for new messages")
        folder_path = self.__get_folder_path(queue.name)
        new_messages = self.__list_files_in_folder(folder_path)
        
        for message_file in new_messages:
          logging.info(f"file {message_file} found")
          message = self.__read_file_contents(queue.name, message_file)
          logging.info(f"New message {message}")
          self.__create_new_message_entry(queue, message)
          self.__delete_file(queue.name, message_file)
      
      time.sleep(1)

  def save(self, queue_name, message):
    queue_folder_path = self.__get_folder_path(queue_name)
    self.__create_folder_if_not_exists(queue_folder_path)
    
    self.__create_file_with_message(message, queue_folder_path)


  def get(self, queue_name, count):
    queue = self.__get_dqueue_item(queue_name)
    head = queue.head
    
    result = []
    current_item = head
    while count > 0 and current_item is not None:
      message = self.__get_message_item(current_item, queue_name)
      self.print_message(message)

      if current_item is None:
         break
       
      result.append({"id": str(message.id), "content": message.content})
      count -= 1
      current_item = message.next_id

    return result
       
    
  def __create_new_message_entry(self, queue, content):
    tail = queue.tail
    head = queue.head
    id = uuid.uuid1()
    
    # add a new entry for message
    Message.create(
       id = id,
       created_date = date.today(),
       state = "VISIBLE",
       content = content,
       queue_name = queue.name,
       prev_id = tail if tail is not None or tail != "" else None
    )
    logging.info(f"new entry in message created with id {id}")
    
    # update previous tail
    if tail is not None and tail != "":
      logging.info(f"tail is not none updating tail")
      Message.objects(id=tail, queue_name=queue.name).update(next_id=str(id))

    # update queue tail
    head = str(id) if head is None else head
    tail = str(id)
    logging.info(f"updating head and tail of queue {queue} to head {head} tail {tail}")

    # we can optimize to do batch updat on queue table
    visible_message_count = queue.visible_messages + 1
    DQueue.objects(name=queue.name).update(head=head, tail=tail, visible_messages=visible_message_count)

  def __get_folder_path(self, queue_name):
    return  self.raw_file_path_prefix + queue_name

  def __create_folder_if_not_exists(self, folder_path):
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      logging.info(f"Folder '{folder_path}' created.")
    else:
      logging.info(f"Folder '{folder_path}' already exists.")
        
  def __read_file_contents(self, queue_name, file_path):
      full_path = self.__get_folder_path(queue_name) + "/" + file_path
      logging.info(f"reading file contents from {full_path}")
      try:
          with open(full_path, 'r') as file:
              contents = file.read()
              return contents
      except FileNotFoundError:
          logging.info("File not found. Please check the file path.")
      except Exception as e:
          logging.info(f"An error occurred: {e}")

  def __create_file_with_message(self, message, folder_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}"
    full_path = folder_path + "/" + filename
    
    with open(full_path, "w") as file:
        file.write(message)
    
    logging.info(f"File '{filename}' created with message.")
    
  def __list_files_in_folder(self, folder_path):
    try:
        return sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    except FileNotFoundError:
        return []
    
  def __delete_file(self, queue_name, file_path):
    full_path = self.__get_folder_path(queue_name) + "/" + file_path
    file = Path(full_path)
    try:
        file.unlink()
        logging.info(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        logging.info(f"File '{file_path}' not found.")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
    
  def __get_dqueue_item(self, queue_name):
    try:
        item = DQueue.objects.get(name=queue_name)
        return item
    except DQueue.DoesNotExist:
        logging.info(f"No item found with name: {queue_name}")
        return None

  def __get_message_item(self, message_id, queue_name):
    try:
        item = Message.objects.get(id=message_id, queue_name=queue_name)
        return item
    except DQueue.DoesNotExist:
        logging.info(f"No item found with name: {message_id}")
        return None
    
  def print_message(self, entry):
    logging.info(entry.id)
    logging.info(entry.created_date)
    logging.info(entry.state)
    logging.info(entry.content)
    logging.info(entry.queue_name)
    logging.info(entry.prev_id)
    logging.info(entry.next_id)
    


  