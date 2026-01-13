import httpx
from fastapi import HTTPException

async def validate_breed(breed: str):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.thecatapi.com/v1/breeds")
        breeds = [b["name"] for b in response.json()]
        if breed not in breeds:
            raise HTTPException(status_code=400, detail="Invalid breed")
        return True