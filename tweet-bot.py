import asyncio
import tweepy
import random
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# open the list of the words

async def tweeter():
    while True:
        with open('list.txt', "r") as f:
            lines = [line.rstrip('\n') for line in f if line != '\n']

        shuffled_lines = random.sample(lines, len(lines))

        for shuffledline in shuffled_lines:
            try:
                api.update_status(shuffledline)
                lines.remove(shuffledline)
                with open('list.txt', "w") as f:
                    for line in lines:
                        f.write(line + "\n")

            except tweepy.TweepError as e:
                print(e.reason)
            await asyncio.sleep(39000)


# because heroku restarts daily, no need to create a for loop to refresh page

async def retweeter():
    while True:
        for tweet in api.user_timeline(screen_name='MerriamWebster', count=6):
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    print("time until next retweet session: 10000s")
                    await asyncio.sleep(10000)

                    break
            except tweepy.TweepError as e:
                print(e)

        for tweet in api.user_timeline(screen_name='Dictionarycom', count=5):
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    print("time until next retweet session: 10000s")
                    await asyncio.sleep(10000)
                    break
            except tweepy.TweepError as e:
                print(e)

        for tweet in api.user_timeline(screen_name='Thesauruscom', count=5):
            try:
                if "#SynonymOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    print("time until next retweet session: 10000s")
                    await asyncio.sleep(10000)
                    break

            except tweepy.TweepError as e:
                print(e)

        for tweet in api.user_timeline(screen_name='OED', count=2):
            try:
                if "Word of the Day" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    print("time until next retweet session: 10000s")
                    await asyncio.sleep(10000)
                    break

            except tweepy.TweepError as e:
                print(e)

        await asyncio.sleep(10000)


async def main():
    task1 = asyncio.create_task(tweeter())
    task2 = asyncio.create_task(retweeter())
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
