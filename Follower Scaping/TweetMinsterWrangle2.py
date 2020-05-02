#####################################################################################
#### Sort through each account to check which ones follow 20% of the Anchor List ####
#####################################################################################
# This takes a very long time (several days) so it was used in concert with TweetMinsterUpload2 for remote monitoring
import datetime
import ftplib
import logging
import pandas as pd
import time
import tweepy
import sys

#Redirecting output + erorr to single file for remote monitoring
sys.stdout = open('InfluenceWrangle.log', 'a')
sys.stderr = sys.stdout
#Formating logging
logging.basicConfig(format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s')

#Upload Influencer list on addition
def uploadfile(filename):
    session = ftplib.FTP_TLS('ftp.aclearvote.co', 'TwitterSphere@aclearvote.co', 'TwitterSphere')
    file = open(filename, 'rb')
    filemsg = "STOR " + filename
    session.storbinary(filemsg, file)
    file.close()
    session.quit()


##Adding data to print output, probably more efficent way of doing this..
def addtofile(message):
    x = str(datetime.datetime.now())
    message = x + " " + message
    print(message)

## Connecting to twitter API, returning False if fails to authenticate
def connect():
    auth = tweepy.OAuthHandler("k6zQPVJcqCNSdxhiEfCHxSZyd", "CSzTcURWlfof7QjpIbgxWBF2LaHHaE8Fv8C7N1RS3IJVNZxNNf")
    auth.set_access_token("819161304669847553-Uhxs5EgaAvwHpS0l1yutpjf0JUnqVhv",
                          "R6YFwcCeilUGen6vfubW1vdIc5VVNk4nTT4WGBuTCEe27")
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        addtofile("Authentication OK")
        return auth
    except:
        addtofile("Error during authentication")
        return False

## Main Program
def mainquery():
    # get list of potentials
    BNOCS = pd.read_csv('BNOCS.csv')
    # get Anchor group
    Anchor = pd.read_csv('TweetMinsterList.csv')
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
        BNOCS.to_csv('BNOCS.csv', index=False)
        # start main operation
        x = 0
        user_name = BNOCS.loc[i, "handle"]
        msg = "Trawling " + user_name + "'s friends ..."
        addtofile(msg)
        msg = "Number " + str(i) + " of " + end
        addtofile(msg)
        ## specify in API to wait on rate limit and give it as Warning so can be seen in log file
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        # use Cursor object to download page of 200 friends at a time
        for page in tweepy.Cursor(api.friends, screen_name=user_name, count=200).pages():
            # cycle through each page of 200 looking for Anchors, update counter with each one
            for friend in page:
                handle = friend._json["screen_name"]
                if Anchor['Handle'].str.contains(handle).any():
                    x = x + 1
            # as soon as counter reaches threshhold (20%) update and move on, stops unnecessary API calls
            if x > 16:
                msg = user_name + " qualified. Added to list."
                addtofile(msg)
                # create temporary DataFrame, add data
                df = pd.DataFrame([[BNOCS.loc[i, "name"], BNOCS.loc[i, "handle"], BNOCS.loc[i, "description"],BNOCS.loc[i, "followers_count"], BNOCS.loc[i, "friends_count"],BNOCS.loc[i, "listed_count"], BNOCS.loc[i, "favourites_count"],BNOCS.loc[i, "created_at"], BNOCS.loc[i, "features"]]],columns=['name', 'handle', 'description', 'followers_count', 'friends_count','listed_count', 'favourites_count', 'created_at', 'features'])
                # download base DF and append temporary dataframe to the bottom
                BNOCS1 = pd.read_csv("BNOCS1.csv")
                NewList1 = BNOCS1.append(df)
                #update base DF then upload to server
                NewList1.to_csv('BNOCS1.csv', index=False)
                uploadfile("BNOCS1.csv")
                break
        # If after all friends cycled, doesnt reach threshold, skip and add to log
        if x <= 16:
            msg = user_name + " does not qualify."
            addtofile(msg)
    # return true on completion
    return True

#main
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
        except:
            print("Some other error...")
            time.sleep(300)
            pass