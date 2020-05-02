#######################################################################
#### Get All Followers of Each Twitter account in TweetMinster List ####
########################################################################
import pandas as pd
import tweepy
import csv

def clearstring(var):
    forbiddenCHar = ["@", "\n"]
    for char in forbiddenCHar:
        if char in var:
            var = var.replace(char, '')
    return var



def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth)
    friends = []
    num = 0
    for page in tweepy.Cursor(api.friends, screen_name=user_name, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, count=200).pages():
        try:
            print("Turning Page ... " + str(num))
            numf = num * 200
            print("Downloaded " + str(numf) + " friends")
            try:
                friends.extend(page)
            except:
                print("Waiting before turning page")
                time.sleep(60)
                friends.extend(page)
            num = num + 1
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return friends
def save_followers_to_csv(user_name, data):
    """
    saves json data to csv
    :param data: data recieved from twitter
    :return: None
    """
    HEADERS = ["name", "screen_name", "description", "followers_count", "followers_count",
               'friends_count', "listed_count", "favourites_count", "created_at"]
    with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)


TweetMinsterList = pd.read_csv('TweetMinsterList.csv')
Outdata = pd.read_csv('InfluencerList.csv')
auth = tweepy.OAuthHandler()
auth.set_access_token()

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

x = 0
for i in range(0,len(TweetMinsterList["Handle"])):
    if TweetMinsterList.loc[i, "Loc"] == "x":
        x = i
for i in range(x,len(TweetMinsterList["Handle"])):
    username = clearstring(TweetMinsterList.loc[i, "Handle"])
    print("Collecting " + username + "'s followings")
    print("Number " + str(i) + " of 87")
    TweetMinsterList.loc[TweetMinsterList["Loc"] == "x", "Loc"] = ""
    TweetMinsterList.loc[i, "Loc"] = "x"
    TweetMinsterList.to_csv('TweetMinsterList.csv', index=False)
    friends = get_followers(username)
    save_followers_to_csv(username, friends)
    print("Success")