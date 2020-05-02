#####################################
#### Use Model to analyse tweets ####
#####################################


import fasttext
from DataCleaner import *
import pandas as pd

model = fasttext.load_model('model-en.ftz')
BnocList = pd.read_csv("BNOCSFINAL1.csv")
tweets = pd.read_csv("tweets.csv", sep=r'\s*,\s*',header=0, engine='python')
columns = ["conversation_id", "created_at", "timezone", "user_id", "place", "retweet", "quote_url", "video", "near", "geo", "source", "user_rt_id", "user_rt", "retweet_id", "retweet_date", "translate", "trans_src", "trans_dest"]
tc = 0

for i in range(0, len(BnocList["handle"])):
    handle = BnocList.loc[i, "handle"]
    filepath = "tweets/" + handle + "_tweets.csv"
    tweetlist = pd.read_csv(filepath)
    for column in columns:
        tweetlist = tweetlist.drop(column, 1)
    tweets = tweets.append(tweetlist, ignore_index=True)
    #print(tweets["id"])
    tlen = len(tweetlist["username"])
    if i%10 == 0:
        print (str(i) + " users completed.")
    if tlen > 200:
        tlen = 200
    for x in range(0, tlen):
        tc = tc + 1
        if tc % 1000 == 0:
            print(str(tc) + " tweets done.")
        tweet = tweetlist.loc[x, "tweet"]
        id = tweetlist.loc[x, "id"]
        #print(id)
        #print(tweets.loc[tweets["id"] == id, "Negative"])
        tweet = correct(tweet)
        sentiment = model.predict(tweet, k=3)
        #print(sentiment)
        for y in range(0, len(sentiment[0])):
            label = sentiment[0][y]
            if label == "__label__NEGATIVE":
                tweets.loc[tweets["id"] == id, "Negative"] = sentiment[1][y]
            if label == "__label__POSITIVE":
                tweets.loc[tweets["id"] == id, "Positive"] = sentiment[1][y]
            if label == "__label__NEUTRAL":
                tweets.loc[tweets["id"] == id, "Neutral"] = sentiment[1][y]
    tweets.to_csv("tweets.csv", index=False)








