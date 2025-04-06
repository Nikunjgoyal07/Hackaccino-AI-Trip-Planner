from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=google_api_key) # Using locally hosted Gemma3
getreccomendations = APIRouter()

class TripPlanRequest(BaseModel):
    travel_mode: str = Field(..., description="Best travel option based on budget (Flight/Train/Bus)")
    hotel_type: str = Field(..., description="Recommended hotel type (Budget/Mid-Range/Luxury)")
    location_details: str = Field(..., description="Suggested locality to stay in for convenience and budget")
    food_recommendation: str = Field(..., description="Best food options within the budget")
    activities_recommendation: str = Field(..., description="Suggested activities and must-visit places")

parser = PydanticOutputParser(pydantic_object=TripPlanRequest)

@getreccomendations.get("/getreccomendations")
async def get_trip_budget(
    request: Request,
    from_city: str = Query(...),
    destination_city: str = Query(...),
    num_days: int = Query(...),
    interests: str = Query(...),
    max_budget: int = Query(...)  # Strict budget constraint
):
    print(f"Generating optimized travel plan for {num_days} days in {destination_city} within {max_budget} INR...")

    # Directly ask LLM for the best travel plan
    template = PromptTemplate(
        input_variables=["from_city", "destination_city", "num_days", "max_budget"],
        template="""
        You are an expert travel planner. Plan a {num_days}-day trip from {from_city} to {destination_city} within a strict budget of {max_budget} INR.

        Optimize the trip by selecting:
        - **Best mode of transportation** (Flight, Train, or Bus) based on budget.
        - **Best hotel type** (Budget, Mid-Range, or Luxury) and a good locality to stay.
        - **Food recommendation** (Street food, mid-range restaurants, fine dining).
        - **Top activities** (Must-visit places within budget).

        **Return the response in this JSON format:**
        {format_instruction}
        """,
        partial_variables={"format_instruction": parser.get_format_instructions()}
    )

    chain = template | model | parser

    # Invoke the LLM to generate an optimized travel plan
    result = chain.invoke({
        "from_city": from_city,
        "destination_city": destination_city,
        "num_days": num_days,
        "max_budget": max_budget
    })
    print(result)

    return result
