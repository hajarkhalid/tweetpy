import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import redis
from rq import Queue
from worker import post_tweet_job  # import from worker.py
from rq.job import Job

load_dotenv()

app = FastAPI()

redis_conn = redis.Redis(host='localhost', port=6379, db=0)
queue = Queue('tweets', connection=redis_conn)

@app.post("/tweet/")
async def tweet_endpoint(
    text: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    job = queue.enqueue(post_tweet_job, text, content)
    return JSONResponse(content={"message": "Tweet is being posted.", "job_id": job.id})

@app.get("/status/{job_id}")
def get_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {"status": job.get_status(), "result": job.result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"status": "OK", "message": "Twitter FastAPI Bot is running"}
