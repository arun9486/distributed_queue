from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from infra import Message
from infra import DQueue

KEYSPACE = "default"

def list_table_names(session):
  query = f"SELECT table_name FROM system_schema.tables WHERE keyspace_name='{KEYSPACE}'"
  rows = session.execute(query)
  table_names = [row.table_name for row in rows]
  print(f"Tables in keyspace '{KEYSPACE}':", table_names)
  return table_names

# Fetch and print all entries in the DQueue table
def list_all_messages():
    all_entries = Message.objects.all()  # Retrieve all entries
    for entry in all_entries:
      print()
      print_message(entry)
      
def print_message(entry):
  print(entry.id)
  print(entry.created_date)
  print(entry.state)
  print(entry.content)
  print(entry.queue_name)
  print(entry.prev_id)
  print(entry.next_id)

def list_all_queues():
  all_entries = DQueue.objects.all()  # Retrieve all entries
  for entry in all_entries:
    print()
    print(entry.name)
    print(entry.id)
    print(entry.state)
    print(entry.retention_time)
    print(entry.visible_messages)
    print(entry.inprogress_messages)
    print(entry.head)
    print(entry.tail)
    
  