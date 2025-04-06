from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=google_api_key)
getfoods = APIRouter()

class FoodRecommendationRequest(BaseModel):
    class FoodInfo(BaseModel):
        name: str = Field(..., description="Name of the food")
        description: str = Field(..., description="Short 1-2 line description of the food")

    list_of_foods: list[FoodInfo] = Field(
        default_factory=list, description="List of most popular cultural foods with descriptions"
    )

parser = PydanticOutputParser(pydantic_object=FoodRecommendationRequest)

def search_top_foods(destination_city: str):
    """
    Searches DuckDuckGo for the most popular cultural foods in the destination city.
    """
    search_tool = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    query = f"Most popular cultural foods in {destination_city}"
    return search_tool.run(query)


@getfoods.get("/getfoods")
async def get_food_recommendation(
    request: Request,
    destination_city: str = Query(...)
):
    print(f"Destination: {destination_city}")

    # Fetch search results for top cultural foods
    search_results = search_top_foods(destination_city)

    # Convert search results into text format
    formatted_results = "\n".join(search_results) if search_results else "No search results found."

    # Updated prompt with real food data
    template = PromptTemplate(
        input_variables=["destination_city", "search_results"],
        template="""
        You are a food travel assistant. Based on the provided search results, suggest a list of the **most popular cultural foods** to try in {destination_city}.
        
        Search Results:
        {search_results}

        Please format your response as a JSON object following this structure:
        {format_instruction}
        """,
        partial_variables={"format_instruction": parser.get_format_instructions()}
    )

    chain = template | model | parser

    # Invoke model with real search results
    result = chain.invoke({"destination_city": destination_city, "search_results": formatted_results})
    print(result)

    return result