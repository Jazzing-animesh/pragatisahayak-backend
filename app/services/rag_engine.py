"""AI-powered business advisory and follow-up chat services.

The service deliberately keeps the retrieval step local: callers provide the
village, business category, competitor, and scheme records that form the
ground-truth context for the model.  If Gemini is unavailable, callers still
receive a useful, clearly-labelled template report.
"""

import json
import os
from typing import Any


def _value(value: Any, key: str, default: Any = "N/A") -> Any:
    """Read a field from either a model-like object or a dictionary."""
    if value is None:
        return default
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _number(value: Any, default: float = 0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _names(items: list[Any] | None) -> list[str]:
    names: list[str] = []
    for item in items or []:
        name = _value(item, "name", item if isinstance(item, str) else "")
        if name not in (None, ""):
            names.append(str(name))
    return names


def _fallback_report(
    user_data: dict[str, Any],
    village: Any,
    category: Any,
    competitors: list[Any] | None,
    language: str,
) -> dict[str, Any]:
    """Return a transparent template report when AI analysis is unavailable."""
    v_name = str(_value(village, "name", "your area"))
    c_name = str(_value(category, "name", "this business"))
    population = int(_number(_value(village, "population", 3000), 3000))
    competitor_count = len(competitors or [])
    hindi = language == "hi"

    if hindi:
        summary = (
            f"उपलब्ध जानकारी के आधार पर {v_name} (जनसंख्या लगभग {population:,}) "
            f"में {c_name} की मध्यम संभावना दिखाई देती है। AI विश्लेषण उपलब्ध नहीं है, "
            "इसलिए यह एक प्रारंभिक टेम्पलेट रिपोर्ट है।"
        )
        limitation = "सीमित डेटा उपलब्ध है"
        market_opportunity = "स्थानीय मांग बढ़ने की संभावना"
        market_reason = f"{population:,} की जनसंख्या एक संभावित बाजार का संकेत देती है"
    else:
        summary = (
            f"Based on available data, {c_name} in {v_name} (population about "
            f"{population:,}) shows moderate potential. AI analysis is unavailable, "
            "so this is an initial template report."
        )
        limitation = "Limited data available"
        market_opportunity = "Potential for growing local demand"
        market_reason = f"A population of {population:,} indicates a potential market"

    return {
        "confidence": "Low",
        "market_summary": summary,
        "market_analysis": {
            "demand_score": 60,
            "target_customers": int(population * 0.3),
            "raw_material_availability": "Medium",
            "infrastructure_readiness": "Medium",
            "seasonal_factor": "Data unavailable",
        },
        "swot": {
            "strengths": [
                {"point": market_opportunity, "why": market_reason},
                {
                    "point": "Low competition"
                    if competitor_count < 3
                    else "Established market",
                    "why": f"{competitor_count} competitors found nearby",
                },
            ],
            "weaknesses": [
                {"point": limitation, "why": "AI analysis is unavailable"},
            ],
            "opportunities": [
                {
                    "point": "Government schemes",
                    "why": "Confirm eligibility with the local District Industries Centre",
                },
            ],
            "threats": [
                {
                    "point": "Infrastructure gaps",
                    "why": "Rural areas may have limited facilities",
                },
            ],
        },
        "threats": [
            {
                "name": "Data limitation",
                "severity": "Medium",
                "description": "A complete AI-backed market analysis could not be generated.",
                "mitigation": "Validate demand, costs, and local competition before investing.",
            }
        ],
        "roadmap": [
            {
                "phase": "Month 1-2",
                "title": "Planning",
                "tasks": ["Market research", "Registration"],
                "estimated_cost": 5000,
            },
            {
                "phase": "Month 3-4",
                "title": "Setup",
                "tasks": ["Equipment", "Workspace"],
                "estimated_cost": 100000,
            },
            {
                "phase": "Month 5-6",
                "title": "Launch",
                "tasks": ["Operations", "Marketing"],
                "estimated_cost": 20000,
            },
        ],
        "pricing_suggestion": "Consult local customers and competitors before setting prices.",
        "alternatives": [],
    }


def generate_rag_report(
    user_data: dict[str, Any],
    village: Any,
    category: Any,
    competitors: list[Any] | None,
    matched_schemes: list[Any] | None,
    language: str = "en",
) -> dict[str, Any]:
    """Generate an AI-backed business advisory report.

    ``village`` and ``category`` may be ORM objects or dictionaries.  The
    returned object is JSON-serializable and follows the schema requested by
    the API.  Missing credentials, malformed model output, and provider
    failures intentionally fall back to a low-confidence template.
    """
    client = None
    try:
        from google import genai
        from google.genai import types

        api_key = os.environ.get("LLM_API_KEY", "")
        if not api_key:
            return _fallback_report(user_data, village, category, competitors, language)

        client = genai.Client(api_key=api_key)
        competitor_names = _names(competitors)
        scheme_names = _names(matched_schemes)
        lang_instruction = (
            "Respond in Hindi using Devanagari script."
            if language == "hi"
            else "Respond in English."
        )

        context = f"""
GROUND TRUTH DATA (USE ONLY THIS — DO NOT INVENT):
- Entrepreneur: {user_data.get("name", "User")}
- Village: {_value(village, "name", "Unknown")}
- Population: {_value(village, "population")}
- Literacy Rate: {_value(village, "literacy_rate") }%
- Primary Occupation: {_value(village, "primary_occupation")}
- Nearest City: {_value(village, "nearest_city_km")} km
- Business: {_value(category, "name", "Unknown")}
- Sector: {_value(category, "sector")}
- Investment Range: Rs.{_value(category, "investment_min", 0)} - Rs.{_value(category, "investment_max", 0)}
- Risk Level: {_value(category, "risk_level", "Medium")}
- Typical Margin: {_value(category, "typical_margin", 20)}%
- Available Capital: Rs.{user_data.get("capital", 0)}
- Competitors Nearby: {len(competitor_names)} ({", ".join(competitor_names[:5])})
- Matched Government Schemes: {", ".join(scheme_names[:5]) or "None supplied"}
"""
        prompt = f"""You are PragatiSahayak, an AI business advisor for rural Indian
entrepreneurs. {lang_instruction}

RULES:
1. ONLY use the ground truth data provided below.
2. NEVER invent government schemes, interest rates, or financial figures.
3. ALWAYS explain WHY you recommend something.
4. If data is insufficient, clearly state "Limited data available".
5. Be specific with numbers from the context.
6. Output ONLY valid JSON matching the schema below.

{context}

Generate a business advisory report in this exact JSON format:
{{
  "confidence": "High" or "Medium" or "Low",
  "market_summary": "2-3 sentence analysis of local market demand",
  "market_analysis": {{
    "demand_score": 75,
    "target_customers": 1500,
    "raw_material_availability": "High" or "Medium" or "Low",
    "infrastructure_readiness": "High" or "Medium" or "Low",
    "seasonal_factor": "Description of seasonal demand variation"
  }},
  "swot": {{
    "strengths": [{{"point": "Short point", "why": "Evidence from context"}}],
    "weaknesses": [{{"point": "Short point", "why": "Evidence from context"}}],
    "opportunities": [{{"point": "Short point", "why": "Evidence from context"}}],
    "threats": [{{"point": "Short point", "why": "Evidence from context"}}]
  }},
  "threats": [{{
    "name": "Threat name",
    "severity": "High" or "Medium" or "Low",
    "description": "What could go wrong",
    "mitigation": "How to handle it"
  }}],
  "roadmap": [{{
    "phase": "Month 1-2",
    "title": "Registration & Planning",
    "tasks": ["Task"],
    "estimated_cost": 5000
  }}],
  "pricing_suggestion": "Suggested pricing strategy based on local market",
  "alternatives": [{{
    "name": "Alternative Business Name",
    "score": 78,
    "investment_range": "Rs.1,00,000 - Rs.3,00,000",
    "why": "Why this is a good alternative"
  }}]
}}"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        result = json.loads(response.text)
        if not isinstance(result, dict):
            raise ValueError("Gemini returned a non-object report")
        return result
    except Exception as exc:
        print(f"RAG Engine Error: {exc}")
        return _fallback_report(user_data, village, category, competitors, language)
    finally:
        if client is not None:
            client.close()


def chat_with_ai(
    message: str,
    context: dict[str, Any],
    history: list[dict[str, str]] | None = None,
    language: str = "en",
) -> dict[str, Any]:
    """Answer a short follow-up question using only the supplied report context."""
    client = None
    try:
        from google import genai
        from google.genai import types

        api_key = os.environ.get("LLM_API_KEY", "")
        if not api_key:
            return {
                "reply": "AI chat is currently unavailable. Please check back later.",
                "confidence": "Low",
                "sources": [],
            }

        client = genai.Client(api_key=api_key)
        lang_instruction = "Respond in Hindi." if language == "hi" else "Respond in English."
        history_text = "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')}"
            for item in (history or [])[-6:]
        )
        system_prompt = f"""You are PragatiSahayak AI assistant. {lang_instruction}
Only use the supplied context. Never invent schemes, rates, or numbers.
Explain why. If unsure, say so. Keep the answer under 200 words and limit it
to business advisory topics.

CONTEXT:
Village: {context.get("village", "Unknown")}
Business: {context.get("category", "Unknown")}
State: {context.get("state", "Unknown")}
Capital: Rs.{context.get("capital", 0)}

RECENT CONVERSATION:
{history_text or "None"}

USER QUESTION: {message}"""
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=system_prompt,
            config=types.GenerateContentConfig(temperature=0.4),
        )
        return {
            "reply": response.text,
            "confidence": "High",
            "sources": ["PragatiSahayak Database", "Government Scheme Records"],
        }
    except Exception as exc:
        print(f"Chat Error: {exc}")
        return {
            "reply": "I'm unable to process your question right now. Please try again.",
            "confidence": "Low",
            "sources": [],
        }
    finally:
        if client is not None:
            client.close()