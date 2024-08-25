from fastapi import FastAPI

from routes import scrape

app = FastAPI()
app.include_router(scrape.router)
