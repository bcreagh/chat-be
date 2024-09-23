from fastapi import FastAPI
from pydantic_settings import BaseSettings
from ai import chatgpt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from bot.bots import BotService
import json
from ukrainian_word_stress import Stressifier, StressSymbol

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
	bot = BotService.get_bot(req.bot)
	resp = chatgpt.callChatgpt(bot.prompt.replace("$INPUT", req.input).replace("$FORMAT", json.dumps(bot.answer_format)))
	parsed_resp = json.loads(resp)
	stressify = Stressifier(on_ambiguity="all", stress_symbol=StressSymbol.CombiningAcuteAccent)
	parsed_resp["stressed"] = stressify(parsed_resp["ukrainian"])
	return parsed_resp

class BotConfigReq(BaseModel):
    name: str

@app.get("/botconfigs")
def botConfigs():
	return BotService.get_bots()

class TranscriptReq(BaseModel):
    transcript: str
    name: str

@app.post("/transcript")
def transcript(req: TranscriptReq):
	resp = chatgpt.callChatgpt(req.transcript + 
	"""
					 
		The content above is a transcript from an educational video. Take that content, and:
		
		1) Present the content in the style of an informative textbook in the Ukrainian language
		2) Give a series of questions and answers in the Ukrainian language based on the content that could be used as flashcards

		Your answer should be in json format. Please only give raw json, do not add any prefixes or suffixes to the json.

		The json should be in the following format:

		{
			"content": "<content of the video in the style of an informative textbook, formatted in markdown.>",
			"questions": [
				{
					"question": "<question 1>",
					"answer": "<answer 1>"
				},
				{
					"question": "<question 2>",
					"answer": "<answer 2>"
				}
			]
		}
	""")
	stressify = Stressifier(on_ambiguity="all", stress_symbol=StressSymbol.CombiningAcuteAccent)
	result = json.loads(resp)
	contents_file_name = f"./storage/{req.name}.md"
	with open(contents_file_name, "w") as file:
		file.write(stressify(result["content"]))
	questions_file_name = f"./storage/{req.name}.txt"
	with open(questions_file_name, "w") as file:
		for q in result["questions"]:
			file.write(f"{stressify(q['question'])};{stressify(q['answer'])}\n")
	return {"message": "success"}