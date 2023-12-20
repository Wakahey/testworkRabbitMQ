import asyncio
import websockets
import json

async def listen_results():
    uri = "ws://0.0.0.0:8765/listen_results"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    result_json = await websocket.recv()
                    result = json.loads(result_json)
                    input_text = result.get("input", "")
                    output_text = result.get("output", "")
                    print(f"Received result: input: {input_text}, output: {output_text}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed. Reconnecting...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_results())
