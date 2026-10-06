from pydantic import BaseModel


class Topic(BaseModel):
    slug: str
    label: str
