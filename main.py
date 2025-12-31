import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

app = FastAPI(title="Gemini Chatbot API")

# Initialize Gemini model (free tier)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

chat_history = []

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    chat_history.append(HumanMessage(content=request.message))

    result = llm.invoke(chat_history)

    chat_history.append(AIMessage(content=result.content))

    return ChatResponse(response=result.content)
