from dataclasses import dataclass
from typing import Literal
from pydantic import BaseModel, Field
from rich.prompt import Prompt
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage, UsageLimits
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import logfire

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

logfire.configure(send_to_logfire='if-token-present')

class ItemDetails(BaseModel):
    item_name: str
    item_price: float
    item_url: str
    
class Shopping_list(BaseModel):
    items_list: list
    
@dataclass
class Deps:
    web_page_text: str

search_agent = Agent[Deps](
    'groq:llama-3.3-70b-versatile',
    result_type=ItemDetails,
    retries=3,
    system_prompt="You are a shopping assistant. Your goals is to find the best prices for the items given.",
    instrument=True,
)

extraction_agent = Agent(
    'groq:llama-3.3-70b-versatile',
    result_type=list[ItemDetails],
    system_prompt="Extract all item information from the given text."
)

usage_limits = UsageLimits(request_limit=15)

def get_search_url(site: str, query: str) -> str:
    query_str = query.replace(" ", "+")
    if site.lower() == "bestbuy":
        return f"https://www.bestbuy.com/site/searchpage.jsp?st={query_str}"
    elif site.lower() == "newegg":
        return f"https://www.newegg.com/p/pl?d={query_str}"
    elif site.lower() == "walmart":
        return f"https://www.walmart.com/search?q={query_str}"
    return ""


def get_site_selectors(site: str) -> dict:
    if site.lower() == "bestbuy":
        return {
            "item": ".sku-item",
            "title": ".sku-title",
            "price": ".priceView-customer-price span",
            "link": ".sku-title a"
        }
    elif site.lower() == "newegg":
        return {
            "item": ".item-cell",
            "title": ".item-title",
            "price": ".price-current",
            "link": ".item-title"
        }
    elif site.lower() == "walmart":
        return {
            "item": "div[data-item-id]",
            "title": "a[data-type='itemTitles']",
            "price": "span[data-automation-id='product-price']",
            "link": "a[data-type='itemTitles']"
        }
    return {}

@search_agent.tool
async def extract_items(ctx: RunContext[Deps]) -> list[ItemDetails]:
    result = await extraction_agent.run(ctx.deps.web_page_text, usage=ctx.usage)
    logfire.info(f"Extracted items: {result}")
    return result.data

@search_agent.tool
async def scrape_product_site(site_name: str, search_query: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        search_url = get_search_url(site_name, search_query)
        if not search_url:
            return f"Search URL not supported for site: {site_name}"

        await page.goto(search_url)
        await page.wait_for_timeout(3000)  # Wait for page content to load

        selectors = get_site_selectors(site_name)
        if not selectors:
            return f"No selectors defined for site: {site_name}"

        items = await page.query_selector_all(selectors['item'])
        results = []
        for item in items[:5]:  # Limit to top 5 products
            try:
                title = await item.locator(selectors['title']).text_content()
                price = await item.locator(selectors['price']).text_content()
                link = await item.locator(selectors['link']).get_attribute("href")
                results.append({
                    "title": title.strip() if title else "N/A",
                    "price": price.strip() if price else "N/A",
                    "url": link if link.startswith("http") else f"https://{site_name}.com{link}"
                })
            except Exception:
                continue

        await browser.close()
        return results


@app.post("/search_items/")
async def search_items(shopping_list: Shopping_list):
    items = shopping_list.items_list
    items_text = "\n".join(items)
    deps = Deps(web_page_text=items_text)
    result = await search_agent.run(deps, usage=Usage(usage_limits))
    return result.data