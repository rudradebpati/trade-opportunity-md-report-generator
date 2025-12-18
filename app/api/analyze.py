from fastapi import APIRouter, Depends, Request
from app.security.auth import verify_api_key
from app.security.rate_limiter import limiter
from app.services.search_service import fetch_market_news
from app.services.ai_service import analyze_with_llm
from app.utils.markdown import generate_markdown

router = APIRouter()

@router.get("/analyze/{sector}")
@limiter.limit("5/minute")
async def analyze_sector(sector: str, request:Request, api_key=Depends(verify_api_key)):
    """
    Analyze the Indian {sector} sector using Gemini 2.5 Flash.

    This endpoint will return a trade opportunity report in Markdown format.
    The report will include current trends, specific trade opportunities, and critical risks.

    Parameters:
        sector (str): The sector to analyze.

    Returns:
        dict: A JSON object with the analysis, following the MarketAnalysis schema.
    """
    market_data = await fetch_market_news(sector)
    analysis = await analyze_with_llm(sector, market_data)
    report = generate_markdown(sector, analysis)
    return {"report": report}
