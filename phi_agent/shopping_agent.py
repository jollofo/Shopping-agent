from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from phi.agent import Agent, RunResponse
from phi.utils.pprint import pprint_run_response
from phi.model.deepseek import DeepSeekChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from web_scraper import WebScraper
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000"   # Python Backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class Shopping_list(BaseModel):
    items_list: list

@app.get("/")
async def root():
    {"message": "A-ok"}

    
@app.post("/search_items/")
async def search_items(shopping_list: Shopping_list):
    sites = {"bestbuy", "newegg", "walmart", "target", "etsy", ""}
    web_agent = Agent(
        name="Web Agent",
        # model=DeepSeekChat(),
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo(), WebScraper()],
        description="You are a shopping assistant. Your goal is to help users find the best deals on the items they are trying to buy.",
        instructions=["For a given item, find at least 3 online stores to recommend with links to the specific items.",
                      "Try to be as specific as possible with the links you provide and provide only the links",
                      "Feed each url into the web scraper and return the results"],
        show_tool_calls=True,
        markdown=True
    )

    response: RunResponse = web_agent.run(f"Give recommendations of stores where I can buy the items in this list: {shopping_list}.", stream=False)
    pprint_run_response(response, markdown=True)

    return response