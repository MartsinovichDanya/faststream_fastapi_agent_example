from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream.kafka import KafkaBroker
from pydantic import BaseModel


broker = KafkaBroker("localhost:9092")


class MessageRequest(BaseModel):
    msg: str


@broker.subscriber("result")
async def base_handler(body):
    print(body)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.stop()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/send_message")
async def send_message(request: MessageRequest):
    await broker.publish(request.msg, topic="process")
    return {"status": "Message sent", "msg": request.msg}
