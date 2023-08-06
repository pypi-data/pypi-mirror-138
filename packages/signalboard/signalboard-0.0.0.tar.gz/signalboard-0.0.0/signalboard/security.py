from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header(...)):
    """
    This is not used yet in app, example usage in secured_health api router
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
