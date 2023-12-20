from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.post("/queue_reverse_text")
async def queue_reverse_text(request: TextRequest):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='text_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='text_queue',
        body=request.text,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )

    connection.close()
    return {"message": "Text queued for processing"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
