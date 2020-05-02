#####################################################################################################
#### Filter through downloaded followers to sort out only those who are followed by at least 20% ####
#####################################################################################################
import pandas as pd
import tweepy


def clearstring(var):
    forbiddenCHar = ["@", "\n"]
    for char in forbiddenCHar:
        if char in var:
            var = var.replace(char, '')
    return var
TweetMinsterList = pd.read_csv('TweetMinsterList.csv')


InfluencerList = pd.DataFrame([["none", "none", "none", "none", "none", "none", "none", "none", 0 ]], columns=['name', 'handle', 'description', 'followers_count','friends_count', 'listed_count', 'favourites_count', 'created_at', 'features'])
for i in range(0,len(TweetMinsterList["Handle"])):
    username = clearstring(TweetMinsterList.loc[i, "Handle"])
    userlist = [username]
    csvname = username + "_followers.csv"
    potentials = pd.read_csv(csvname)
    print("loaded " + username + "'s friends")
    print("(Number " + str(i) + " of 87)")
    for x in range (0,len(potentials["name"])):
        if potentials.loc[x, "followers_count"] > 50000:
            name = potentials.loc[x, "name"]
            handle = potentials.loc[x, "screen_name"]
            # print("Possible Candidate: " + name)
            if InfluencerList['handle'].str.contains(handle).any():
                #print ("Already mentioned ... Updated")
                features = InfluencerList.loc[InfluencerList["handle"] == handle, "features"]
                #print(features)
                features = features + 1
                InfluencerList.loc[InfluencerList["handle"] == handle, "features"] = features
            else:
                #print("Not Mentioned, Added !")
                df = pd.DataFrame([[name,potentials.loc[x, "screen_name"], potentials.loc[x, "description"], potentials.loc[x, "followers_count"], potentials.loc[x, "friends_count"], potentials.loc[x, "listed_count"], potentials.loc[x, "favourites_count"], potentials.loc[x, "created_at"], 0]], columns=['name', 'handle', 'description', 'followers_count','friends_count', 'listed_count', 'favourites_count', 'created_at', 'features'])
                InfluencerList = InfluencerList.append(df)
    #print("Potentials so far: ")
print("Filtering...")
InfluencerList = InfluencerList[InfluencerList.features > 16]
InfluencerList = InfluencerList[InfluencerList.friends_count > 100]
InfluencerList = InfluencerList[InfluencerList.friends_count < 11000]
InfluencerList.to_csv('BNOCS.csv', index=False)
print("Success")