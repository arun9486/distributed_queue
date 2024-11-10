import xmlrpc.client

# Connect to the server
server_url = "http://localhost:8000"
client = xmlrpc.client.ServerProxy(server_url)

# Make remote procedure calls
x, y = 5, 3
print(f"The result of add({x}, {y}) is: {client.add(x, y)}")
print(f"The result of subtract({x}, {y}) is: {client.subtract(x, y)}")