from cassandra.cluster import Cluster

from utils import KEYSPACE

# Connect to the Cassandra cluster
cluster = Cluster(['localhost'])  # replace with your host IP
session = cluster.connect()

# Specify the keyspace and table you want to drop
tables = ['dqueue', 'message']

# Use the specified keyspace
session.set_keyspace(KEYSPACE)

# Construct and execute the DROP TABLE query
for table_name in tables:
  drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
  session.execute(drop_table_query)
  print(f"Table {table_name} has been dropped from keyspace {KEYSPACE}.")

# Close the connection
cluster.shutdown()