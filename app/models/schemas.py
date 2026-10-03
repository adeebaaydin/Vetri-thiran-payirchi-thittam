from typing import Literal

from pydantic import BaseModel, Field


PlannerName = Literal[
    "home",
    "party",
    "jewelry"
]


class UserCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: str = Field(
        min_length=5,
        max_length=160
    )

    password: str = Field(
        min_length=6,
        max_length=128
    )


class UserLogin(BaseModel):

    email: str

    password: str


class Recommendation(BaseModel):

    title: str

    category: str

    description: str

    estimated_price: float = Field(
        ge=0
    )

    platform: str

    search_url: str

    why_it_fits: str


class PlannerResponse(BaseModel):

    planner: str

    budget: float

    budget_allocation: dict[str, float]

    summary: str

    recommendations: list[Recommendation]

    tips: list[str]

    ai_used: bool = False


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    rooms: list[str] = Field(
        min_length=1
    )

    style: str = "modern"

    notes: str = ""


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = "birthday"

    venue: str = "home"

    city: str = ""

    notes: str = ""


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = "wedding"

    style: str = "elegant"

    outfit_color: str = ""

    notes: str = ""