from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.getplaces import getplaces
from routes.getfoods import getfoods
from routes.getreccomendations import getreccomendations
from routes.getactivities import getactivities
from routes.get_cafes import cafes_router
from routes.get_fine_dining import fine_dining_router
from routes.get_street_food import streetfood_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all heades
)

app.include_router(getplaces, tags=["getplaces"])
app.include_router(getfoods, tags=["getfoods"])
app.include_router(getreccomendations, tags=["getreccomendations"])
app.include_router(getactivities, tags=["getactivities"])
app.include_router(cafes_router, tags=["cafes"])
app.include_router(fine_dining_router, tags=["fine_dining"])
app.include_router(streetfood_router, tags=["street_food"])