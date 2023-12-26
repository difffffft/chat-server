class BasePlugin:

    def __init__(self):
        self.name = None
        self.description = None
        self.params = None

    def info(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.params
            },
        }

    def run(self, params: dict):
        pass
