import pandas as pd
#########################################
### Wrangle TweetMinster List into CSV ###
##########################################

def clearstring(var):
    forbiddenCHar = ["@", "\n"]
    for char in forbiddenCHar:
        if char in var:
            var = var.replace(char, '')
    return var
outdata = pd.read_csv('TweetMinsterList.csv')
f = open("twitterlist.txt", "r")
i = 0
y = 0
for x in f:
    if i == 0:
        outdata.loc[y, "Name"] = x
    if i == 1:
        outdata.loc[y, "Handle"] = clearstring(x)
    if i == 2:
        outdata.loc[y, "Bio"] = x

    if i == 2:
        i = 0
        y = y + 1
    else:
        i = i + 1
    outdata.to_csv('TweetMinsterList.csv', index=False)