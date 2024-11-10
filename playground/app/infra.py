from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table

from utils import KEYSPACE


cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Create the keyspace if it doesn't exist
session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
""")

print(f"Keyspace '{KEYSPACE}' created or verified.")

# Connect to the cluster
connection.setup(['127.0.0.1'], KEYSPACE, protocol_version=3)

# Define a model
class DQueue(Model):
    __keyspace__ = KEYSPACE 
    name = columns.Text(primary_key=True)
    id = columns.UUID(primary_key=True)
    state = columns.Text()
    retention_time = columns.Integer()
    visible_messages = columns.Integer()
    inprogress_messages = columns.Integer()
    head = columns.Text()
    
class Message(Model):
    __keyspace__ = KEYSPACE 
    id = columns.UUID(partition_key=True)
    created_date = columns.Date(primary_key=True)
    state = columns.Text()                   
    queue_name = columns.Text(primary_key=True)
    next_id = columns.Text()
    prev_id = columns.Text()
    host = columns.Text()
    
sync_table(DQueue)
sync_table(Message)