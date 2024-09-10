import json
from bot.bot import Bot
import os

_bots = {}
_bot_dir = './bot/config'

def _get_filenames(directory):
    filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filenames.append(filename)
    return filenames

def _create_bot_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        name = data.get('name')
        prompt = data.get('prompt')
        answer_format = data.get('answer_format')
        hidden_fields = data.get('hidden_fields')
        return Bot(name, prompt, answer_format, hidden_fields)

def _populate_bots():
    bot_files = _get_filenames(_bot_dir)
    for bot_file in bot_files:
        bot = _create_bot_from_json(f'{_bot_dir}/{bot_file}')
        _bots[bot.name] = bot

_populate_bots()

class _BotService:
    def get_bot(self, bot_name) -> Bot:
        return _bots.get(bot_name)
    
    def get_bots(self) -> dict:
        return _bots

BotService = _BotService()