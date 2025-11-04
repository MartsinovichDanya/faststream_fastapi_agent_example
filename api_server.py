import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from faststream.kafka import KafkaBroker
import uvicorn
import uuid

from models import ChatRequest, ChatResponse, Message, CheckRequest, CheckResponse


broker = KafkaBroker("localhost:9092")

messages_answered = {}

@broker.subscriber("result")
async def msg_handler(msg: Message):
    messages_answered[msg.req_id] = msg.text
    print(messages_answered)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def index():
    with open(os.path.join(static_dir, "dev_index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/logs")
async def index():
    with open("logs/app.log", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/send_message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    req_id = str(uuid.uuid4())
    await broker.publish(Message(req_id=req_id, text=request.msg), topic="process")
    return ChatResponse(req_id=req_id)


@app.post("/check_status", response_model=CheckResponse)
async def send_message(request: CheckRequest):
    if request.req_id not in messages_answered:
        return CheckResponse(req_id=request.req_id,
                             status="processing",
                             result=None)
    result = messages_answered[request.req_id]
    del messages_answered[request.req_id]
    return CheckResponse(req_id=request.req_id,
                         status="done",
                         result=result)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_config="config/log.ini")
