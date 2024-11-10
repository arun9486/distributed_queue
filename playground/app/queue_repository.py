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
    self.__create_dqueue_entry(name, retention_time, id)
    logging.info(f"Item {id} created in queue table")
    return id
    
  def __create_dqueue_entry(self, name, retention_time, id):
    return DQueue.create(
        name=name,
        id=id,
        state="CREATED",
        retention_time=retention_time,             
        visible_messages=0,
        inprogress_messages=0 
    )
    
