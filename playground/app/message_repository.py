from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
import uuid
from utils import KEYSPACE
from infra import DQueue
import logging

class MessageRepository():
  def send(self, queue_name, messaeg):
    print("Not implemented")
    
  def receive(self, id):
    print("Not implemented")
  
  def delete(self, id):
    print("Not implemented")

  