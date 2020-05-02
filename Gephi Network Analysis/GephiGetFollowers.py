############################################################################
# I realised that for accurate network analysis I would need all
# the followers for all accounts examined so had to start again with this.
############################################################################
# This takes a very long time so used with GephiUpload for remote monitoring

import tweepy
import csv
import time
import datetime
import ftplib
import logging
import pandas as pd
import sys

#1 Configure Logging

sys.stdout = open('GetFollowers.log', 'a')
sys.stderr = sys.stdout
#Formating logging
logging.basicConfig(format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s')

def uploadfile(filename):
    session = ftplib.FTP_TLS()
    file = open(filename, 'rb')
    filemsg = "STOR " + filename
    session.storbinary(filemsg, file)
    file.close()
    session.quit()

def addtofile(message):
    x = str(datetime.datetime.now())
    message = x + " " + message
    print(message)

def clearstring(var):
    forbiddenCHar = ["@", "\n"]
    for char in forbiddenCHar:
        if char in var:
            var = var.replace(char, '')
    return var

def connect():
    auth = tweepy.OAuthHandler()
    auth.set_access_token()
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        addtofile("Authentication OK")
        return auth
    except:
        addtofile("Error during authentication")
        return False

def save_followers_to_csv(user_name, data):
    """
    saves json data to csv
    :param data: data recieved from twitter
    :return: None
    """
    HEADERS = ["name", "screen_name", "description", "followers_count", "followers_count",
               'friends_count', "listed_count", "favourites_count", "created_at"]
    filepath = user_name + "_followers.csv"
    with open(filepath, 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)
    uploadfile(filepath)

def mainquery():
    # get list of potentials
    BNOCS = pd.read_csv('GephiList.csv')
    AnchorList = pd.read_csv("TweetMinsterList.csv")
    # try to connect, if not pass up
    auth = connect()
    if not auth:
        return 0
    # ensures that program restarts from where it left of in case of breakdown
    for i in range(0, len(BNOCS["handle"])):
        if BNOCS.loc[i, "Loc"] == "x":
            x = i
    # main loop
    for i in range(x, len(BNOCS["handle"])):
        # Update location of loop each cycle
        BNOCS.loc[BNOCS["Loc"] == "x", "Loc"] = ""
        BNOCS.loc[i, "Loc"] = "x"
        end = str(len(BNOCS["handle"]))
        BNOCS.to_csv('GephiList.csv', index=False)
        # start main operation
        x = 0
        user_name = BNOCS.loc[i, "handle"]
        friends_count = BNOCS.loc[i, "friends_count"]
        if friends_count > 10000:
            addtofile(user_name + " has too many friends so skip.")
            continue
        Anch = AnchorList["Handle"].values
        if user_name in Anch:
            addtofile(user_name + " is anchor so skip.")
            continue

        msg = "Trawling " + user_name + "'s friends ..."
        addtofile(msg)
        msg = "Number " + str(i) + " of " + end
        addtofile(msg)
        friends = []
        ## specify in API to wait on rate limit and give it as Warning so can be seen in log file
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        for page in tweepy.Cursor(api.friends, screen_name=user_name, count=200).pages():
            friends.extend(page)
        save_followers_to_csv(user_name, friends)
        addtofile("Downloaded " + user_name + "'s friends.")
    return True

if __name__ == '__main__':
    while True:
        try:
            mainquery()
            # if completed break infinte loop
            if mainquery() == True:
                print("Completed!")
                break
            # if failed authentication, most likely internet issue, wait 15 mins retry, add to log
            if mainquery() == 0:
                addtofile("Cant connect, waiting 15 minutes to retry.")
                time.sleep(900)
        # API error, usually failed query, wait 5 minutes before restart
        except tweepy.TweepError:
            print("tweepy.TweepError=")
            time.sleep(300)
            pass
        # something else, wait 5 mins, will be in log file, if internet then will catch on loop
        except Exception as e:
            print(str(e))
            print("Some other error...")
            time.sleep(300)
            pass
