from cassandra.cqlengine import connection
from cassandra.cqlengine.management import drop_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

# Define the model (schema definition for reference)
class Messages(Model):
    __keyspace__ = "default"
    name = columns.UUID(primary_key=True)
    state = columns.Text(primary_key=True)
    created_date = columns.Date(primary_key=True)
    id = columns.UUID()
    host = columns.Text()

# Connect to the Cassandra cluster and keyspace
connection.setup(['127.0.0.1'], "default", protocol_version=3)

# Drop the table
drop_table(Messages)
print("Table 'Messages' has been deleted.")
