from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster

from utils import KEYSPACE

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Specify your keyspace

# Query to list all tables in the keyspace
query = f"SELECT table_name FROM system_schema.tables WHERE keyspace_name='{KEYSPACE}'"
rows = session.execute(query)

# Print all table names
table_names = [row.table_name for row in rows]
print(f"Tables in keyspace '{KEYSPACE}':", table_names)

# Close the connection
cluster.shutdown()
