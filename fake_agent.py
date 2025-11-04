from time import sleep


class Agent:
    def __init__(self):
        pass

    def invoke(self, msg: str):
        sleep(2)
        return f"🤖 ответ {msg}"
