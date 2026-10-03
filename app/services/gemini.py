import json
import logging

from app.config import settings

from app.models.schemas import PlannerResponse

from app.services.fallback import (
    home_fallback,
    party_fallback,
    jewelry_fallback,
)


logger = logging.getLogger(__name__)


def get_client():

    if (
        not settings.google_api_key
        or not settings.ai_enabled
    ):
        return None

    from google import genai

    return genai.Client(
        api_key=settings.google_api_key
    )


def build_prompt(
    planner: str,
    data: dict
) -> str:

    return f"""
You are PocketSmart AI, a careful budget recommendation assistant.

Planner:
{planner}

User input:

{json.dumps(
    data,
    ensure_ascii=False,
    indent=2
)}

Create a realistic, budget-aware plan.

Important rules:

1. Do not claim that a specific product is currently in stock.
2. Do not claim that prices are live.
3. Prices must be presented as estimates.
4. Platform names are shopping/service search destinations.
5. Stay within the user's budget.
6. Give practical recommendations.
7. Give 3 to 6 recommendations.
8. Keep recommendations relevant to the planner.

Return ONLY valid JSON in this structure:

{{
    "planner": "{planner}",
    "budget": number,

    "budget_allocation": {{
        "category": number
    }},

    "summary": "string",

    "recommendations": [

        {{
            "title": "string",
            "category": "string",
            "description": "string",
            "estimated_price": number,
            "platform": "Amazon",
            "search_url": "https://www.google.com/search?q=...",
            "why_it_fits": "string"
        }}

    ],

    "tips": [
        "string",
        "string",
        "string"
    ],

    "ai_used": true
}}

The total major budget allocations must not exceed the user's budget.
"""


def parse_response(text: str) -> dict:

    text = text.strip()

    if text.startswith("```"):

        parts = text.split(
            "\n",
            1
        )

        if len(parts) == 2:

            text = parts[1]

        if "```" in text:

            text = text.rsplit(
                "```",
                1
            )[0]

    return json.loads(text)


async def generate(
    planner: str,
    data,
    image_bytes: bytes | None = None,
    mime_type: str | None = None,
) -> PlannerResponse:

    fallback_functions = {

        "home":
            home_fallback,

        "party":
            party_fallback,

        "jewelry":
            jewelry_fallback,
    }

    fallback = fallback_functions[planner](data)

    client = get_client()

    if client is None:

        return fallback

    try:

        prompt = build_prompt(
            planner,
            data.model_dump()
        )

        contents = [
            prompt
        ]

        if image_bytes:

            from google.genai import types

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=(
                        mime_type
                        or "image/jpeg"
                    ),
                )
            )

            contents.append(
                """
Analyze the uploaded outfit image only for
broad color and style coordination.

Do not identify the person.
"""
            )

        response = client.models.generate_content(

            model=settings.gemini_model,

            contents=contents,

            config={
                "response_mime_type":
                    "application/json"
            },
        )

        parsed = parse_response(
            response.text
        )

        return PlannerResponse.model_validate(
            parsed
        )

    except Exception as exc:

        logger.exception(
            "Gemini request failed. "
            "Using fallback: %s",
            exc,
        )

        return fallback