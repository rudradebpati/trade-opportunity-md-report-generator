from duckduckgo_search import DDGS
from datetime import datetime

async def fetch_market_news(sector: str):
    current_date= datetime.today()
    try:
        query = f"{sector} India market trends trade opportunities for {str(current_date.month)}, {str(current_date.year)}"
        
        # 'ddgs' is a wrapper that handles proxies and headers for you
        with DDGS() as ddgs:
            # We fetch 'text' results which are already cleaned of HTML
            results = ddgs.text(query, region="in-en", timelimit="m", max_results=5)
            
            # Combine snippets into a clean string for Gemini
            news_feed = "\n\n".join([
                f"Title: {r['title']}\nSnippet: {r['body']}" 
                for r in results
            ])
            
            return news_feed if news_feed else "No recent news found."
            
    except Exception as e:
        print(f"Scraping error: {e}")
        return "Market data temporarily unavailable."