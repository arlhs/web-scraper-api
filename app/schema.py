from pydantic import BaseModel

class UrlPages(BaseModel):
    url: str
    pages: int