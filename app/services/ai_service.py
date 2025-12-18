from pydantic import BaseModel
from google import genai
from google.genai import types
from app.services.system_prompt import get_system_prompt

class MarketAnalysis(BaseModel):
    summary: str
    opportunities: list[str]
    risks: list[str]
    sentiment: str

async def analyze_with_llm(sector: str, market_data: str):
    # Combine user instruction with the scraped data
    """
    Analyze the Indian {sector} sector using Gemini 2.5 Flash.

    Combine user instruction with the scraped market data to identify current trends, specific trade opportunities, and critical risks.

    Args:
        sector (str): The sector to analyze.
        market_data (str): Scraped market data.

    Returns:
        str: JSON output with the analysis, following the MarketAnalysis schema.
    """
    prompt = f"""
    Analyze the Indian {sector} sector.
    
    Using this scraped market data:
    {market_data}

    Identify current trends, specific trade opportunities, and critical risks.
    """

    client = genai.Client()

    # Use 'response_schema' to enforce valid JSON output
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_prompt(),
            response_mime_type="application/json",
            response_schema=MarketAnalysis,
        ),
    )

    return response.parsed.model_dump()