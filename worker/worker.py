import aio_pika
import asyncio
import json
import logging

async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        text = message.body.decode()
        reversed_text = text[::-1]
        await send_result(text, reversed_text)
        print(f"Received message: {text}, Reversed: {reversed_text}")

async def send_result(text, result):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()

    await channel.declare_queue('result_queue', durable=True)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps({"input": text, "output": result}).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key='result_queue'
    )

    await connection.close()

async def start_consuming():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()

    queue = await channel.declare_queue('text_queue', durable=True)

    await queue.consume(callback)

    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted. Stopping...')

    await connection.close()

if __name__ == "__main__":
    asyncio.run(start_consuming())
