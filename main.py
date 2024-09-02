from fastapi import FastAPI
from pydantic_settings import BaseSettings
from ai import chatgpt
from pydantic import BaseModel

class Settings(BaseSettings):
	chatgpt_key: str

settings = Settings()
app = FastAPI()

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