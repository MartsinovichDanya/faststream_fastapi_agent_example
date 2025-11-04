import asyncio

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker

from fake_agent import Agent
from models import Message

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
