# from fastapi import Header, HTTPException


# async def get_token_header(x_token: str = Header()):
#     if x_token != "zaeem":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def get_query_token(token: str):
#     if token != "talha":
#         raise HTTPException(status_code=400, detail="No token provided")
