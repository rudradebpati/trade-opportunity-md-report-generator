def generate_markdown(sector: str, analysis: dict):
    # Use .join() to handle dynamic list lengths without index errors
    opportunities_list = "\n".join([f"- {opt}" for opt in analysis.get('opportunities', [])])
    risks_list = "\n".join([f"- {risk}" for risk in analysis.get('risks', [])])

    return f"""
# 🇮🇳 Trade Opportunity Report: {sector.title()} Sector

## 📝 Market Summary
{analysis.get('summary', 'No summary available.')}

## 🚀 Key Opportunities
{opportunities_list if opportunities_list else "- No specific opportunities identified."}

## ⚠️ Risks & Challenges
{risks_list if risks_list else "- No major risks identified."}

---
*Disclaimer: Not SEBI registered advice. Data analyzed via Gemini 2.5 Flash.*
"""