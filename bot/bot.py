class Bot:
    def __init__(self, name: str, prompt: str, answer_format: dict, hidden_fields: list):
        self.name = name
        self.prompt = prompt
        self.hidden_fields = hidden_fields
        self.answer_format = answer_format