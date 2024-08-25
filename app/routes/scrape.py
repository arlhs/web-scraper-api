from fastapi import APIRouter, Depends
from service.scrape import ScrapeService
from schema import UrlPages

from auth import authenticate
router = APIRouter()

@router.post("/scrape/")
async def scrapeRouter(urlpage: UrlPages, token: str = Depends(authenticate)):
    return await ScrapeService.scrape(urlpage)

