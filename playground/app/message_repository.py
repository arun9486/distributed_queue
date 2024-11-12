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
import time
from datetime import datetime
import threading
import time
from utils import list_table_names
from infra import DQueue
from infra import Message
from datetime import date
from pathlib import Path
import heapq

class MessageRepository():
  def __init__(self):
    self.raw_file_path_prefix = "/home/arun-linux/cassandra/raw_message/"
    scan_thread = threading.Thread(target=self.scan_messages)
    scan_thread.start()

    visible_thread = threading.Thread(target=self.visible_messages)
    visible_thread.start()

    self.invisible_pq = dict()
    self.invisible_dict= dict()
    

  def visible_messages(self):
    while True:
      queues = DQueue.objects.all()
      for queue in queues:
        if "CREATED" != queue.state:
          continue

        invisible_queue = self.invisible_pq.get(queue.name)
        if not invisible_queue:
           continue 
         
        retention_time = queue.retention_time
        current_time = time.time()
        while invisible_queue and current_time - invisible_queue[0][0] > retention_time:
          current_item = heapq.heappop(invisible_queue)
          _, message = current_item
          logging.info(f"Trying to put message {message.id} back to queue")

          if message.id in self.invisible_dict.get(queue.name):
            self.__put_back_message_entry(queue, message)
            time.sleep(0.5)
    
      time.sleep(1)

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
    logging.info("Before receive queue contents")
    self.__print_queue(queue)
    head = queue.head
    
    result = []
    current_item = head
    actual_count = 0
    
    if  queue_name not in self.invisible_pq:
      self.invisible_pq[queue_name] = []

    if  queue_name not in self.invisible_dict:
      self.invisible_dict[queue_name] = set()
      
    while count > 0 and current_item is not None:
      message = self.__get_message_item(current_item, queue_name)
      self.__print_message(message)
      
      if message is None:
        logging.info("This should not be happening, there is current_item but message is null")
        break
       
      date = time.time()
      self.invisible_dict[queue_name].add(message.id)
      heapq.heappush(self.invisible_pq[queue_name], (date, message))
      result.append({"id": str(message.id), "content": message.content})
      count -= 1; actual_count += 1; current_item = message.next_id


    head = None
    if current_item is not None:
      head = current_item

    # update head with new value and new visibile message count
    visible_message_count = queue.visible_messages - actual_count
    inprogress_count = queue.inprogress_messages + actual_count

    Message.objects(id=head, queue_name=queue.name).update(prev_id = None)
    DQueue.objects(name=queue.name).update(head=head, visible_messages=visible_message_count, inprogress_messages=inprogress_count)

    # debugging
    logging.info("After receive queue contents")
    self.__print_queue(queue)
    return result

def delete(self, queue_name, message_id):
    invisible_dict = self.invisible_dict.get(queue_name)
    
    if not invisible_dict:
      return

    if message_id in invisible_dict:
      invisible_dict.remove(message_id)
      self.__delete_message_item(message_id, queue_name)
  def __put_back_message_entry(self, queue, message):
    # get the latest item
    queue = self.__get_queue_item(queue.name)
    tail = queue.tail
    head = queue.head
    id = message.id

    prev_id = tail if tail is not None or tail != "" else None
    Message.objects(id=message.id, queue_name=queue.name).update(prev_id = prev_id, next_id = None)

    # update previous tail
    if tail is not None and tail != "":
      logging.info(f"tail is not none updating tail")
      Message.objects(id=tail, queue_name=queue.name).update(next_id=str(id))

    # update queue tail
    head = str(id) if head is None else head
    tail = str(id)
    logging.info(f"updating head and tail of queue {queue} to head {head} tail {tail}")

    # we can optimize to do batch updat on queue table
    logging.info(f"Visible message before adding back {queue.visible_messages}")
    visible_message_count = queue.visible_messages + 1
    invisible_message_count = queue.inprogress_messages - 1
    DQueue.objects(name=queue.name).update(head=head, tail=tail, visible_messages=visible_message_count, inprogress_messages=invisible_message_count)
    
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

  def __get_queue_item(self, name):
    try:
        item = DQueue.objects.get(name=name)
        return item
    except DQueue.DoesNotExist:
        logging.info(f"No item found with name: {queue_id}")
        return None
      
  def __delete_message_item(self, id, queue_name):
    try:
        Message.objects(id=id, queue_name=queue_name).delete()
        logging.info(f"Message with id {id} and queue_name {queue_name} has been deleted.")
    except Exception as e:
        logging.info(f"Failed to delete message: {e}")
    
  def __print_message(self, entry):
    logging.info(entry.id)
    logging.info(entry.created_date)
    logging.info(entry.state)
    logging.info(entry.content)
    logging.info(entry.queue_name)
    logging.info(entry.prev_id)
    logging.info(entry.next_id)
    

  def __print_queue(self, entry):
    logging.info(entry.id)
    logging.info(entry.state)
    logging.info(entry.retention_time)
    logging.info(entry.visible_messages)
    logging.info(entry.inprogress_messages)
    logging.info(entry.head)
    logging.info(entry.tail)
    


  