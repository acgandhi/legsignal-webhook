import time
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

app = FastAPI()

verify_token = os.environ.get("VERIFY_TOKEN")


@app.post("/webhook")
async def webhook(body: dict):
    print(body, type(body))


@app.get('/webhook', response_class=PlainTextResponse)
def rates(
    mode: str = Query(..., alias="hub.mode"), 
    token: str = Query(..., alias="hub.verify_token"), 
    challenge: str = Query(..., alias="hub.challenge")
):
    if (mode == "subscribe" and token == verify_token):
        print("Token Verified")
        return challenge
    else:
        raise HTTPException(status_code=403)


# Docker health check
@app.get("/health")
async def health():
    return f"I'm healthy!{time.time()}"
