# sendOrder.py
import sys
import pika
import json # import json module

# Get the arguments from the command line
username = sys.argv[1]
endpoint = sys.argv[2]
side = sys.argv[3]
quantity = int(sys.argv[4])
price = float(sys.argv[5])

# Create a connection and a channel to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(endpoint))
channel = connection.channel()

# Declare the orders exchange
channel.exchange_declare(exchange="orders", exchange_type="fanout")

# Create an order dictionary with the arguments
order = {
    "username": username,
    "side": side,
    "quantity": quantity,
    "price": price
}

# Convert the order dictionary to a JSON string
order_json = json.dumps(order)

# Send the order to the orders exchange
channel.basic_publish(exchange="orders", routing_key="", body=order_json)
print(f"Sent order: {order}")
channel.close()
connection.close()
