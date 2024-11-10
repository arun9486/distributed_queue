from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster

from utils import KEYSPACE
from utils import list_table_names

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Specify your keyspace
list_table_names(session)

# Close the connection
cluster.shutdown()
