import asyncio
import websockets
import json
from aio_pika import connect_robust

async def listen_results(websocket, path):
    connection = await connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()

    while True:
        result = await get_result(channel)
        try:
            await websocket.send(json.dumps(result))
            print(f"Sent result: {result}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed. Reconnecting...")
            break

async def get_result(channel):
    result_queue = await channel.declare_queue('result_queue', durable=True)

    try:
        message = await result_queue.get()
        if message:
            result = json.loads(message.body.decode())
            return result
    except Exception as e:
        await asyncio.sleep(1)
        print(f"Error getting result: {e}")

    await asyncio.sleep(1)
    return await get_result(channel)

if __name__ == "__main__":
    start_server = websockets.serve(listen_results, "0.0.0.0", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
