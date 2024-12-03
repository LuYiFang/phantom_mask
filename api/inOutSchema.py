from pydantic import BaseModel


class Pharmacy(BaseModel):
    name: str
    open_hours: str
