import os
import time
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import redis
from rq import Queue
import twitter

load_dotenv()

app = FastAPI()

# === Redis Setup ===
redis_conn = redis.Redis(host='localhost', port=6379, db=0)
queue = Queue('tweets', connection=redis_conn)

# === Twitter API Auth ===
api = twitter.Api(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token_key=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    tweet_mode='extended'
)

# === Background Tweet Posting Function ===
def post_tweet_job(text, media_bytes):
    try:
        media = api.UploadMediaChunked(media=media_bytes)
        status = api.PostUpdate(status=text, media=media)
        return {"tweet_id": status.id, "text": status.full_text}
    except Exception as e:
        return {"error": str(e)}

# === FastAPI Route ===
@app.post("/tweet/")
async def tweet_endpoint(
    text: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    job = queue.enqueue(post_tweet_job, text, content)
    return JSONResponse(content={"message": "Tweet is being posted.", "job_id": job.id})

# === Health Check ===
@app.get("/")
def read_root():
    return {"status": "OK", "message": "Twitter FastAPI Bot is running"}
