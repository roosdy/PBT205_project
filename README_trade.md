# Trading App

This is a simple trading app that uses RabbitMQ to send and receive orders and trades.

## Requirements

- Python 3
- pika
- RabbitMQ
- Docker (optional)

## Installation

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```

To install RabbitMQ, you can either download it from the official website or use Docker to run it as a container. For example, you can run:

```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:management
```

This will run RabbitMQ with the management plugin and expose ports 5672 and 15672 to the host machine.

Alternatively, you can use Docker to build and run the trading app as a container. To do this, run:

```bash
docker build -t trading-app .
docker run -d --name trading-app -p 5672:5672 trading-app
```

This will create a trading-app image and run it as a container, exposing port 5672 to the host machine.

## Usage

To start the exchange, run:

```
python exchange.py <endpoint>
```

where `<endpoint>` is the host name or IP address of the RabbitMQ server. For example, if you are running RabbitMQ locally, you can use `localhost` or `127.0.0.1` as the endpoint.

If you are using Docker to run the trading app, you don't need to run this command, as it is already executed when the container launches.

To send an order, run:

```
python sendOrder.py <username> <endpoint> <side> <quantity> <price>
```

where:

- `<username>` is the name of the user who sends the order
- `<endpoint>` is the host name or IP address of the RabbitMQ server
- `<side>` is either `BUY` or `SELL`
- `<quantity>` is an integer representing the number of shares to buy or sell
- `<price>` is a float representing the price per share

For example, you can run:

```
python sendOrder.py Alice localhost BUY 100 10.5
```

This will send an order with username Alice, endpoint localhost, side BUY, quantity 100 and price 10.5.

The exchange will try to match the incoming orders with existing orders in the order book and publish trades to the trades exchange. The trades exchange can be subscribed by other applications or users who are interested in the trade information.

## License

MIT License
