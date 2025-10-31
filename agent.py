from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.chat_models import GigaChat

from prompts import assistant_prompt
from tools import calculator_tool


cert_file_path = "cert/egress_sberca.crt"
key_file_path = "cert/egress_sberca.key"


class Agent:
    def __init__(self):
        self.llm = GigaChat(
            base_url='https://gigachat-ift-preview.sberdevices.delta.sbrf.ru/v1',
            model='GigaChat-Max-preview',
            cert_file=cert_file_path,
            key_file=key_file_path,
            verify_ssl_certs=False,
            temperature=0.1,
            profanity_check=False,
            timeout=600
        )

        self.agent = create_react_agent(
            model=self.llm,
            tools=[calculator_tool],
            prompt=assistant_prompt,
            checkpointer=MemorySaver()
        )

    def invoke(self, msg: str, thread_id: str = "main"):
        config = {"configurable": {"thread_id": thread_id}}
        if msg:
            resp = self.agent.invoke({"messages": [("user", msg)]}, config=config)
            return resp["messages"][-1].content
        return "msg is empty"


if __name__ == '__main__':
    agent = Agent()
    message = f"Привет"
    response = agent.invoke(message)
    print("🤖 :", response)
