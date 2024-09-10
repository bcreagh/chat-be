from fastapi import FastAPI
from pydantic_settings import BaseSettings
from ai import chatgpt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from bot.bots import BotService
import json

class Settings(BaseSettings):
	chatgpt_key: str

settings = Settings()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
	"http://localhost:4200/chat",
	"http://127.0.0.1",
    "http://127.0.0.1:4200",
	"http://127.0.0.1:4200/chat",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
	chatgpt.callChatgpt("Say this is a test")
	return {"message": settings.chatgpt_key[0:5]}


class FreetextReq(BaseModel):
    query: str

@app.post("/freetext")
def freetext(req: FreetextReq):
	resp = chatgpt.callChatgpt(req.query)
	return {"message": resp}

class ChatReq(BaseModel):
    input: str
    bot: str

@app.post("/chat")
def chat(req: ChatReq):
	resp = "asfd"
	bot = BotService.get_bot(req.bot)
	resp = chatgpt.callChatgpt(bot.prompt.replace("$INPUT", req.input).replace("$FORMAT", json.dumps(bot.answer_format)))
	return {"message": resp}

class BotConfigReq(BaseModel):
    name: str

@app.get("/botconfigs")
def botConfigs():
	return BotService.get_bots()