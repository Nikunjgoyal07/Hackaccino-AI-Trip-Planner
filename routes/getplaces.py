from fastapi import APIRouter, Query, Request
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=google_api_key)
getplaces = APIRouter()

# serper_api_key = "df1fbc596384843a27a6ee57ab334f162dd3ed81"

class PlaceRecommendationRequest(BaseModel):
    class PlaceInfo(BaseModel):
        name: str = Field(..., description="Name of the place")
        description: str = Field(..., description="Short 1-2 line description of the place")

    list_of_places: list[PlaceInfo] = Field(
        default_factory=list, description="Recommended list of 10 places to visit with descriptions"
    )

parser = PydanticOutputParser(pydantic_object=PlaceRecommendationRequest)

def search_top_places(destination_city: str):
    """
    Searches DuckDuckGo for the top 10 places to visit in the destination city.
    """
    search_tool = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    query = f"Top 10 places to visit in {destination_city}"
    return search_tool.run(query)


@getplaces.get("/getplaces")
async def get_recommendation(
    request: Request,
    destination_city: str = Query(...)
):
    print(f"Destination: {destination_city}")

    # Fetch search results for top places
    search_results = search_top_places(destination_city)

    # Convert search results into text format
    formatted_results = "\n".join(search_results) if search_results else "No search results found."

    # Updated prompt with real travel data
    template = PromptTemplate(
        input_variables=["destination_city", "search_results"],
        template="""
        You are a travel assistant. Based on the provided search results, suggest a list of the **top 10 places** to visit in {destination_city}.
        
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
