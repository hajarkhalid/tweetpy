import os
from dotenv import load_dotenv
import twitter

load_dotenv()

api = twitter.Api(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token_key=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    tweet_mode='extended'
)

def post_tweet_job(text, media_bytes):
    try:
        media = api.UploadMediaChunked(media=media_bytes)
        status = api.PostUpdate(status=text, media=media)
        return {"tweet_id": status.id, "text": status.full_text}
    except Exception as e:
        return {"error": str(e)}
