from fastapi import FastAPI
from typing import List
from inOutSchema import Pharmacy
import utility as u

app = FastAPI()


@app.get("/api/pharmacies/open", response_model=List[Pharmacy])
def get_open_pharmacies(day: str, time: str):
    return u.get_open_pharmacies(day, time)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
