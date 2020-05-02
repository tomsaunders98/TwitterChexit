
#####################################################
#### Create Gephi Nodes and Edges from this data ####
#####################################################

import pandas as pd
import sys

account_list = pd.read_csv("GephiList.csv")
influencers = pd.read_csv("BNOCSFINAL1.csv")
anchors = pd.read_csv("TweetMinsterList.csv")
GephiNodes = pd.DataFrame(columns=['id', 'label','type_colour'])
GephiEdges = pd.DataFrame(columns=['source', 'target', 'type_colour', 'weight', 'type'])


for i in range(0, len(account_list["handle"])):
    print(str(int(i/len(account_list["handle"])*100)) + "% completed")
    x = len(GephiNodes["id"]) + 1
    handle = account_list.loc[i, "handle"]
    id = account_list.loc[i, "id_account"]
    GephiNodes.loc[x, "id"] = id
    GephiNodes.loc[x, "label"] = account_list.loc[i, "name"]
    Inf = influencers["handle"].values
    Anch = anchors["Handle"].values
    if handle in Inf:
        GephiNodes.loc[x, "type_colour"] = 2
    if handle in Anch:
        GephiNodes.loc[x, "type_colour"] = 1
    if handle not in Anch and handle not in Inf:
        GephiNodes.loc[x, "type_colour"] = 0
    filepath = "followerlist/" + handle + "_followers.csv"
    try:
        followerlist = pd.read_csv(filepath)
    except:
        print("Could not find: " + handle)
    GephiAccount = account_list["handle"].values
    for y in range(0, len(followerlist["screen_name"])):
        handleA = followerlist.loc[y, "screen_name"]
        if handleA in GephiAccount:
            #create edge
            id2 = int(account_list.loc[account_list["handle"] == handleA, "id_account"])
            x = len(GephiEdges["source"]) + 1
            GephiEdges.loc[x, "source"] = id
            GephiEdges.loc[x, "target"] = id2
            GephiEdges.loc[x, "type"] = "directed"
            GephiEdges.loc[x, "weight"] = 1
GephiNodes.to_csv("GephiNodes.csv", index=False)
GephiEdges.to_csv("GephiEdges.csv", index=False)




