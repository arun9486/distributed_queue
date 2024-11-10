from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
import uuid
from utils import KEYSPACE
from infra import DQueue
import logging

class QueueRepository():
  def create(self, name, retention_time):
    id = uuid.uuid1()

    # FIX: creating a new tablefor each queue, can we do better.
    # create a new message table
    self.__create_message_table(name)

    # create an entry in queue metadata table
    self.__create_dqueue_entry(name, retention_time, id)
    
    return id
    
  def __create_dqueue_entry(self, name, retention_time, id):
    item = DQueue.create(
        name=name,
        id=id,
        state="CREATED",
        retention_time=retention_time,             
        visible_messages=0,             
        inprogress_messages=0            
    )

    logging.info(f"Item {item} inserted")

  def __create_message_table(self, queue_name):
      message_table_name = self.__get_message_table_name(queue_name)
      attrs = {
          '__keyspace__': KEYSPACE,
          '__table_name__': message_table_name,
          'id': columns.UUID(partition_key=True, default=uuid.uuid4),  
          'state': columns.Text(primary_key=True),                   
          'created_date': columns.Date(),
          'name': columns.UUID(),
          'host': columns.Text(),
      }

      new_table = type(message_table_name, (Model,), attrs)

      sync_table(new_table)
      logging.info(f"Table '{message_table_name}' created with composite \
                   partition key (id, state) and clustering key \
                   (created_date).")

  def __get_message_table_name(self, table_name):
    return table_name + "_message_table"

