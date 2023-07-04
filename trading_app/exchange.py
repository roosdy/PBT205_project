# exchange.py
import sys
import pika
import json # import json module

# Get the endpoint from the command line
endpoint = sys.argv[1]

# Create a connection and a channel to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(endpoint))
channel = connection.channel()

# Declare the orders and trades exchanges
channel.exchange_declare(exchange="orders", exchange_type="fanout")
channel.exchange_declare(exchange="trades", exchange_type="fanout")

# Create a queue and bind it to the orders exchange
queue_name = channel.queue_declare(queue="", exclusive=True).method.queue
channel.queue_bind(exchange="orders", queue=queue_name)

# Create an empty order book dictionary with two lists for buy and sell orders
order_book = {
    "buy": [],
    "sell": []
}

# Define a function to match orders and publish trades
def match_orders(order):
    # Get the opposite side of the order
    opposite_side = "buy" if order["side"] == "sell" else "sell"
    # Convert the side of the order to lowercase
    side = order["side"].lower()
    # Loop through the opposite side orders in the order book
    for i, opposite_order in enumerate(order_book[opposite_side]):
        # Check if the prices are acceptable for both parties
        if (side == "buy" and order["price"] >= opposite_order["price"]) or \
           (side == "sell" and order["price"] <= opposite_order["price"]):
            # Remove the matched order from the order book
            order_book[opposite_side].pop(i)
            # Create a trade dictionary with the trade information
            trade = {
                "buyer": order["username"] if side == "buy" else opposite_order["username"],
                "seller": order["username"] if side == "sell" else opposite_order["username"],
                "quantity": min(order["quantity"], opposite_order["quantity"]),
                "price": opposite_order["price"]
            }
            # Convert the trade dictionary to a JSON string
            trade_json = json.dumps(trade)
            # Publish the trade to the trades exchange
            channel.basic_publish(exchange="trades", routing_key="", body=trade_json)
            print(f"Published trade: {trade}")
            # Update the quantities of the orders
            order["quantity"] -= trade["quantity"]
            opposite_order["quantity"] -= trade["quantity"]
            # If either order is fully filled, return True
            if order["quantity"] == 0 or opposite_order["quantity"] == 0:
                return True
    # If no match is found, return False
    return False

# Define a callback function to process orders from the orders exchange
def callback(ch, method, properties, body):
    # Receive an order from the orders exchange
    order = json.loads(body) # convert the body from JSON string to dictionary
    print(f"Received order: {order}")
    # Try to match the order with existing orders in the order book
    matched = match_orders(order)
    # If the order is not fully filled, add it to the order book
    if not matched and order["quantity"] > 0:
        # Convert the side of the order to lowercase
        side = order["side"].lower()
        # Add it to the corresponding list in the order book dictionary
        order_book[side].append(order)
        print(f"Added order to the order book: {order}")

# Start consuming messages from the orders exchange
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
