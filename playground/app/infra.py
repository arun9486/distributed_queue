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
    retention_time = columns.Integer()
    visibile_messages = columns.Integer()
    inprogress_messages = columns.Integer()
    
# # FiX it is possible that this wil create hot partition
# class Messages(Model):
#     __keyspace__ = KEYSPACE 
#     name = columns.UUID(primary_key=True)
#     state = columns.Text(primary_key=True)
#     created_date = columns.Date(primary_key=True)
#     id = columns.UUID() 
#     host = columns.Text()
    
#     name = columns.UUID(primary_key=True)            # First part of composite partition key
#     state = columns.Text(primary_key=True)           # Second part of composite partition key
#     created_date = columns.Date(primary_key=True)    # Clustering key
#     id = columns.UUID() 
#     host = columns.Text()

sync_table(DQueue)