#!/usr/bin/env python
import json, tweepy, time
from config import keys


#Authenticate with Twitter API
auth = tweepy.OAuthHandler(keys['consumer_key'],keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)


def getBotFood():

    try:
        #Get signs to tweet out.
        with open('botfood.json', 'r+') as fileOpen:
            json_raw = fileOpen.read()
            json_data = json.loads(json_raw.encode('ascii','ignore').translate(None, '\n\t\r\u'))

            #Delete the signs from botfood.json to prevent duplicate tweets.
            fileOpen.seek(0)
            fileOpen.truncate()
            fileOpen.write("{}")
            fileOpen.close()

        #Create list of strings(aka tweets).
        tweets = []
        for sign in json_data:
            tweets.append(sign + " was just posted! " + json_data[sign] + " up for grabs. http://bit.ly/1TQ2Pys")

        return tweets
    except:
        print "Error: Empty JSON file"
        return None


def postTweets(tweets):
    for tweet in tweets:
        api.update_status(status=tweet)
        time.sleep(10) #Wait 10 seconds.

def main():
    food = getBotFood()
    if food:
        postTweets(food)
    else:
        print "Empty JSON file, no tweets sent."

if __name__ == "__main__":
    main()
