import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def post_tweet_job(text: str, media_content: bytes):
    try:
        # First, upload media if provided
        if media_content:
            media = api.media_upload(filename="media.jpg", file=media_content)
            tweet = api.update_status(status=text, media_ids=[media.media_id])
        else:
            tweet = api.update_status(status=text)

        return {"status": "success", "tweet_id": tweet.id_str}

    except tweepy.TweepError as e:
        return {"status": "error", "message": str(e)}
