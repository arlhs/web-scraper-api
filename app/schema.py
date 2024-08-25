from pydantic import BaseModel, field_validator, Field

class UrlPages(BaseModel):
    url: str
    pages: int = Field(default=1, gt=0)

    @field_validator('pages')
    def check_price(cls, value):
        if value < 1:
            raise ValueError('Page must be greater than 0')
        return value