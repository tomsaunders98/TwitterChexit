###################################
#### Get Followers using Twint ####
###################################
# Free Twitter API only allows Tweets from the last 7 days


import pandas as pd
import twint
import nest_asyncio
import logging
nest_asyncio.apply()
logging.basicConfig(format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s')

def twint_to_pandas(columns):
    return twint.output.panda.Tweets_df[columns]


def mainquery():
    BNOCS = pd.read_csv('BNOCS1.csv')

    for i in range(0, len(BNOCS["handle"])):
        user_name = BNOCS.loc[i, "handle"]

        # c = twint.Config()
        # c.Username = "Case123"
        filename = user_name + "_tweets.csv"
        # c.Custom["tweet"] = ["id", "username", "retweets_count", "likes_count", "date", "hashtags"]
        # c.Output = filename
        # c.Store_csv = True
        #
        # twint.run.Search(c)
        # print(user_name)
        c = twint.Config()
        c.Username = user_name
        c.Limit = 10
        c.Pandas = True
        c.Format = "Username: {username} |  Tweet: {tweet}"
        c.Debug = True
        # Custom output format
        twint.run.Search(c)
        tweettable = twint_to_pandas(["conversation_id", "date", "tweet", "hashtags","nreplies", "nretweets", "nlikes"])

        tweettable.to_csv(filename, index=False)

if __name__ == '__main__':
    mainquery()