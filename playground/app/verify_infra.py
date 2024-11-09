from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Specify the keyspace and table name
keyspace = "default"
table_name = "messages"

# Query system_schema.tables to check if the table exists
table_exists_query = f"""
SELECT * FROM system_schema.tables 
WHERE keyspace_name='{keyspace}' AND table_name='{table_name}';
"""
result = session.execute(table_exists_query)

if result.one():
    print(f"Table '{table_name}' exists in keyspace '{keyspace}'.")
else:
    print(f"Table '{table_name}' does not exist in keyspace '{keyspace}'.")

# Close the cluster connection
cluster.shutdown()
