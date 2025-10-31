import asyncio
from typing import List

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker

from agent import Agent

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)

agent = Agent()


@broker.subscriber("process")
@broker.publisher("result", batch=True)
async def invoke_agent(msg):
    resp = agent.invoke(msg)
    return resp


# @broker.subscriber("response", batch=True)
# async def handle_response(msg: List[str], logger: Logger):
#     logger.info(msg)
#
#
# @app.after_startup
# async def test() -> None:
#     await broker.publish("hi", "test")

if __name__ == "__main__":
    async def main():
        await app.run()
    asyncio.run(main())
