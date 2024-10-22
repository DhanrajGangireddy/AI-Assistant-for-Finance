from fastapi import Header, HTTPException
from configure.config import settings

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.GROQ_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key