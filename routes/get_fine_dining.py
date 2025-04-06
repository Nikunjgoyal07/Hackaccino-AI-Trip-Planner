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
fine_dining_router = APIRouter()

class FineDiningRecommendationRequest(BaseModel):
    class FineDiningInfo(BaseModel):
        name: str = Field(..., description="Restaurant name")
        description: str = Field(..., description="Short 1-2 line description")

    list_of_fine_dining: list[FineDiningInfo] = Field(
        default_factory=list, description="List of 5 recommended fine dining places"
    )

parser = PydanticOutputParser(pydantic_object=FineDiningRecommendationRequest)

def search_fine_dining(destination_city: str):
    search_tool = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    query = f"Best fine dining restaurants in {destination_city}"
    return search_tool.run(query)

@fine_dining_router.get("/getfineDining")
async def get_fine_dining(request: Request, destination_city: str = Query(...)):
    search_results = search_fine_dining(destination_city)
    formatted_results = "\n".join(search_results) if search_results else "No search results found."

    template = PromptTemplate(
        input_variables=["destination_city", "search_results"],
        template=f"""
        You are a travel assistant. Based on the provided search results, suggest a list of the **top 5 fine dining restaurants** in {{destination_city}}.

        Search Results:
        {{search_results}}

        Please format your response as a JSON object following this structure:
        {{format_instruction}}
        """,
        partial_variables={"format_instruction": parser.get_format_instructions()}
    )

    chain = template | model | parser
    result = chain.invoke({"destination_city": destination_city, "search_results": formatted_results})

    return result
