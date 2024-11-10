from cassandra.cqlengine import connection
from cassandra.cqlengine.management import drop_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from utils import KEYSPACE

# Define the model (schema definition for reference)
class DQueue(Model):
    __keyspace__ = KEYSPACE 
    name = columns.Text(primary_key=True)
    id = columns.UUID(primary_key=True)
    retention_time = columns.Integer()
    visibile_messages = columns.Integer()
    inprogress_messages = columns.Integer()
    
# Connect to the Cassandra cluster and keyspace
connection.setup(['127.0.0.1'], "default", protocol_version=3)

# Drop the table
drop_table(DQueue)
print("Table 'DQueue' has been deleted.")
