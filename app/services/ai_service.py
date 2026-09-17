import logging
from pydantic import BaseModel
from google import genai
from google.genai.errors import APIError
from fastapi import HTTPException, status
from app.services.system_prompt import get_system_prompt
from decouple import config

logger = logging.getLogger(__name__)
GEMINI_API_KEY = config("GEMINI_API_KEY")
# LLM_MODEL_NAME=config("LLM_MODEL_NAME")
class MarketAnalysis(BaseModel):
    summary: str
    opportunities: list[str]
    risks: list[str]
    sentiment: str

async def analyze_with_llm(sector: str, market_data: str, model:str):
    # Combine user instruction with the scraped data
    """
    Analyze the Indian {sector} sector using Gemini 2.5 Flash.

    Combine user instruction with the scraped market data to identify current trends, specific trade opportunities, and critical risks.

    Args:
        sector (str): The sector to analyze.
        market_data (str): Scraped market data.

    Returns:
        dict: Parsed market analysis dictionary, following the MarketAnalysis schema.

    Raises:
        HTTPException: If the AI service fails or returns an invalid/empty response.
    """
    prompt = f"""
    Analyze the Indian {sector} sector.
    
    Using this scraped market data:
    {market_data}

    Identify current trends, specific trade opportunities, and critical risks.
    """

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Use 'response_schema' to enforce valid JSON output
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=get_system_prompt(),
                response_mime_type="application/json",
                response_schema=MarketAnalysis,
            ),
        )
        client.close()

        if not response.parsed:
            logger.error("AI model did not return structured data. Response text: %s", getattr(response, 'text', None))
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an empty response or content was filtered by safety policies.",
            )

        return response.parsed.model_dump()

    except APIError as e:
        logger.error("Gemini API error occurred: %s (code: %s)", getattr(e, "message", str(e)), getattr(e, "code", None))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "AI Provider Error",
                "message": getattr(e, "message", str(e)),
                "upstream_code": getattr(e, "code", None),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error during AI analysis: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "AI Processing Error",
                "message": str(e),
            },
        )