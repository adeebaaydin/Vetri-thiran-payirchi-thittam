from urllib.parse import quote_plus

from app.models.schemas import (
    PlannerResponse,
    Recommendation,
)


def link(
    platform: str,
    query: str
) -> str:

    bases = {

        "Amazon":
            "https://www.amazon.in/s?k=",

        "Flipkart":
            "https://www.flipkart.com/search?q=",

        "IKEA":
            "https://www.ikea.com/in/en/search/?q=",

        "Swiggy":
            "https://www.swiggy.com/search?query=",

        "Zomato":
            "https://www.zomato.com/search?q=",

        "OYO":
            "https://www.oyorooms.com/search?location=",
    }

    base = bases.get(
        platform,
        "https://www.google.com/search?q="
    )

    return base + quote_plus(query)


def home_fallback(data) -> PlannerResponse:

    budget = data.budget

    allocation = {

        "furniture":
            round(budget * 0.40, 2),

        "lighting":
            round(budget * 0.15, 2),

        "decor":
            round(budget * 0.20, 2),

        "storage":
            round(budget * 0.15, 2),

        "buffer":
            round(budget * 0.10, 2),
    }

    items = [

        (
            "Compact furniture set",
            "Furniture",
            "Practical furniture suited to the selected rooms.",
            allocation["furniture"] * 0.65,
            "IKEA",
        ),

        (
            "LED lighting bundle",
            "Lighting",
            "Energy-efficient lighting for a simple room refresh.",
            allocation["lighting"] * 0.75,
            "Amazon",
        ),

        (
            "Wall decor set",
            "Decor",
            "Low-cost decorative pieces that can coordinate with the chosen style.",
            allocation["decor"] * 0.50,
            "Flipkart",
        ),

        (
            "Modular storage",
            "Storage",
            "Flexible storage that helps keep rooms organized.",
            allocation["storage"] * 0.80,
            "IKEA",
        ),
    ]

    recommendations = []

    for (
        title,
        category,
        description,
        price,
        platform,
    ) in items:

        recommendations.append(
            Recommendation(
                title=title,
                category=category,
                description=description,
                estimated_price=round(
                    price,
                    2
                ),
                platform=platform,
                search_url=link(
                    platform,
                    title
                ),
                why_it_fits=(
                    f"Fits a {data.style} style and "
                    f"stays within the suggested "
                    f"{category.lower()} allocation."
                ),
            )
        )

    return PlannerResponse(

        planner="home",

        budget=budget,

        budget_allocation=allocation,

        summary=(
            f"A starter home plan for "
            f"{', '.join(data.rooms)} "
            f"using a {data.style} style."
        ),

        recommendations=recommendations,

        tips=[
            "Compare dimensions before buying.",
            "Keep 10% aside for unexpected costs.",
            "Prioritize essential furniture before decorative items.",
        ],

        ai_used=False,
    )


def party_fallback(data) -> PlannerResponse:

    budget = data.budget

    allocation = {

        "food":
            round(budget * 0.45, 2),

        "decoration":
            round(budget * 0.15, 2),

        "venue":
            round(budget * 0.25, 2),

        "entertainment":
            round(budget * 0.10, 2),

        "buffer":
            round(budget * 0.05, 2),
    }

    recommendations = [

        Recommendation(

            title="Catering package search",

            category="Food",

            description=(
                f"Options for approximately "
                f"{data.guests} guests."
            ),

            estimated_price=allocation["food"],

            platform="Swiggy",

            search_url=link(
                "Swiggy",
                data.event_type + " catering"
            ),

            why_it_fits=(
                "Largest share is reserved for food "
                "because guest count drives catering cost."
            ),
        ),

        Recommendation(

            title="Party decoration search",

            category="Decoration",

            description=(
                "Themes and decoration supplies "
                "matching the event."
            ),

            estimated_price=allocation["decoration"],

            platform="Amazon",

            search_url=link(
                "Amazon",
                data.event_type + " party decorations"
            ),

            why_it_fits=(
                "Keeps decorations controlled while "
                "leaving room for food and venue."
            ),
        ),

        Recommendation(

            title="Venue options",

            category="Venue",

            description=(
                f"Venue ideas for {data.event_type} "
                f"in {data.city or 'your area'}."
            ),

            estimated_price=allocation["venue"],

            platform="OYO",

            search_url=link(
                "OYO",
                data.city or "party venue"
            ),

            why_it_fits=(
                "Uses a defined venue allowance "
                "instead of spending the whole budget "
                "on location."
            ),
        ),
    ]

    return PlannerResponse(

        planner="party",

        budget=budget,

        budget_allocation=allocation,

        summary=(
            f"A {data.event_type} plan "
            f"for {data.guests} guests."
        ),

        recommendations=recommendations,

        tips=[
            "Confirm guest count before final catering.",
            "Ask vendors about delivery/setup charges.",
            "Keep a small contingency amount.",
        ],

        ai_used=False,
    )


def jewelry_fallback(data) -> PlannerResponse:

    budget = data.budget

    allocation = {

        "main_piece":
            round(budget * 0.55, 2),

        "secondary_piece":
            round(budget * 0.25, 2),

        "finishing_piece":
            round(budget * 0.15, 2),

        "buffer":
            round(budget * 0.05, 2),
    }

    items = [

        (
            "Statement necklace",
            "Main jewelry",
            "A coordinated statement piece for the selected occasion.",
            allocation["main_piece"],
            "Amazon",
        ),

        (
            "Matching earrings",
            "Earrings",
            "A complementary pair that can echo the outfit color.",
            allocation["secondary_piece"],
            "Flipkart",
        ),

        (
            "Bracelet or bangle",
            "Finishing piece",
            "A simple finishing accessory without exhausting the budget.",
            allocation["finishing_piece"],
            "Amazon",
        ),
    ]

    recommendations = []

    for (
        title,
        category,
        description,
        price,
        platform,
    ) in items:

        recommendations.append(
            Recommendation(

                title=title,

                category=category,

                description=description,

                estimated_price=price,

                platform=platform,

                search_url=link(
                    platform,
                    title
                ),

                why_it_fits=(
                    f"Selected for an "
                    f"{data.occasion} occasion "
                    f"with an {data.style} preference."
                ),
            )
        )

    outfit_text = ""

    if data.outfit_color:

        outfit_text = (
            f" for a {data.outfit_color} outfit."
        )

    return PlannerResponse(

        planner="jewelry",

        budget=budget,

        budget_allocation=allocation,

        summary=(
            f"An {data.occasion} jewelry plan "
            f"in an {data.style} style"
            f"{outfit_text}"
        ),

        recommendations=recommendations,

        tips=[
            "Check material and size details before purchase.",
            "Use the outfit color as a coordination guide.",
            "Compare seller ratings and return policies.",
        ],

        ai_used=False,
    )