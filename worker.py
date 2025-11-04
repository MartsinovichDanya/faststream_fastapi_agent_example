import asyncio
import logging

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker

from fake_agent import Agent
from models import Message


logging.basicConfig(
    filename='static/log.txt',  # Name of the log file
    level=logging.INFO,  # Minimum level of messages to log (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s' # Format of the log messages
)

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)

agent = Agent()


@broker.subscriber("process")
@broker.publisher("result", batch=True)
async def invoke_agent(msg: Message):
    resp = agent.invoke(msg.text)
    return Message(req_id=msg.req_id, text=resp)


if __name__ == "__main__":
    async def main():
        await app.run()
    asyncio.run(main())
