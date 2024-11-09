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
  # message class
  class Messages(Model):
    __keyspace__ = KEYSPACE 
    id = columns.UUID() 
    state = columns.Text(primary_key=True)
    created_date = columns.Date(primary_key=True)
    name = columns.UUID(primary_key=True)
    host = columns.Text()
    
  def create(self, name, retention_period):
    id = uuid.uuid1()

    self.create_dqueue_entry(name, retention_period, id)
    
    # FIX: creating a new table for each queue, can we do better.
    self.create_message_table(name)

  def create_message_table(table_name):
      attrs = {
          '__keyspace__': KEYSPACE,
          '__table_name__': table_name,
          'id': columns.UUID(primary_key=True, default=uuid.uuid4),  
          'state': columns.Text(primary_key=True),                   
          'created_date': columns.Date(primary_key=True),            
          'name': columns.UUID(),
          'host': columns.Text(),
      }

      new_table = type(table_name, (Model,), attrs)

      sync_table(new_table)
      logging.info(f"Table '{table_name}' created with composite partition key (id, state) and clustering key (created_date).")
    
  def create_dqueue_entry(self, name, retention_period, id):
    item = DQueue.create(
        name="queue_name",
        id=uuid.uuid4(),                 
        retention_time=3600,             
        visible_messages=10,             
        inprogress_messages=5            
    )

    logging.info(f"Item {item} inserted")

