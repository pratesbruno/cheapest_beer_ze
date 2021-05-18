from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cheapest_beer_ze.cheapest_beer import get_cheapest_beers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"test": "Test passed."}


@app.get("/get_beers")
def get_beers(address):
    json_response = get_cheapest_beers(address)
    return {"Response": json_response}