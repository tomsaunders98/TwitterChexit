![Logo](https://github.com/tomsaunders98/TwitterChexit/raw/master/web/img/graph.png)
# [Political Twitter](http://twitter.chexit.co.uk/ "Twitter Analysed")
This is all the code for the website [twitter.chexit.co.uk/](http://twitter.chexit.co.uk/) which analyses political twitter.

How it Works
------

This project was worked on over a long period of time and completed in stages. As such, the code (especially the scraping code) has been split up into smaller componenents rather than one larger program as this was originally the way I completed the project. 

Follower Scraping
------
This contains the code for taking a twitter list and then extrapolating a network of linked accounts from that original list. It also contains the code for downloading tweets for this network.

#### Requirements:
* **Python**
* **Twitter API** access + **Tweepy**
		* It isn't easy to do the entire anaylsis in Twint as Twitter will quickly block access if you are trying to download all of the Followers from an account. 
* **Twint**
* **Pandas**

#### Files:
##### 1. TwitterListtoCsv
Converts a Twitter list (copied into a txt file) into a CSV to create a list of anchors. 

##### 2. TweetMinsterGetFollower
Downloads all of the friends of each account in the anchorlist using Tweepy (python wrapper for Twitter API).

##### 3. TweetMinsterWrangle1
Sorts through the list of friends to find those which are followed by at least 20% of Anchors (to create our initial network).

##### 4. TweetMinsterWrangle2 and TweetMinsterUplaod2
To further focus the network, the next criteria was that each member of the larger network either be a) an Anchor or b) follow at least 20% of the Anchors. Since the Network was a lot larger this took a lot longer than the intial Data Wrangling. I kept this code running remotely on a headless Raspberry Pi and the upload file would regularly upload the log file to my FTP server so that I could remotely monitor the program as it wrangled the data.

##### 5. GetTweets
This downloads the last 200 tweets for each account in the smaller network. As the free version of the Twitter API only allows you to download tweets from the last 7 days I had to use Twint in order to download tweets from a much larger range.


Gephi Network Analysis
------

#### Requirements
* **Gephi**
* **Pandas**
* **Tweepy**

#### Files

##### 1. GephiGetFollowers + GephiUpload
To create a network map I needed to download the entire friend list for each account within the network in order to create the edges between nodes. In the original scrape (TweetMinsterWrangle2) I had not downloaded the entire friendlist. Instead, in order to save time, I determined whether an account followed 20% of the Anchors and when this condition was satisfied a moved onto the next account. To do the Gephi mapping I had to revisit this code but instead download **every** friend from each account in the network. 

##### 2. Create Gephi
Gephi works by feeding it a list of nodes (in this case accounts) and edges which link one node to another. In this case the edges were created between two accounts when one followed the other. This code is used to create the edge and node files which can then be loaded into Gephi in order to develop the network map. 

#### Notes
When the files were loaded into Gephi I used Fruchterman Reingold to visualise the initial network for graph.png I and ForceAtlas2 with PreventOverlap to visualise the network for the Visuals. 

The Communities were created using Modularity and the size of the circles were determined using Centrality. 


Sentiment Analysis
------

#### Notes
The 'Divisivity' component on the interactive Graph was developed by analysising the sentiment of all 50,000 tweets and then adding the sentiment ratings to the tweets.csv. the divisity raiting simply does a search of tweets.csv for words containing the phrase in the textbox then takes an average of the neutral rating. This value is used as the base of the 'divisity' rating for a word or phrase.

There are various ways to analyse sentiment of text but the basic NLP techniques (e.g. TextBlob) are not very accurate and can't deal with sarcasm, irony etc. So instead I trained a model using Fasttext, a library for text classification released by Facebook AI Research Lab. 

The model was trained on the [betsentiment dataset](https://github.com/charlesmalafosse/open-dataset-for-sentiment-analysis), the dataaset contains over 6.3 million tweets that have been labelled using the AWS Comprehend API. This dataset was used to train the model that was then applied to the 50,000 tweets that I had collected.


#### Requirements
* **NTLK** (custom stopwords and word_tokenize)
		* I've added the custom stopwords file which preservers sentiment affecting words.
* **BeautifulSoup** (to remove HTML tags etc. from tweets)
* **Fasttext**
		* Model Trainer

#### Files

##### 1. DataCleaner
This cleans the data before it is trained. This includes removing links, converting emojis, removing contractions, correcting spellings, removing punctuation and removing stopwords.

##### 2. TweetSorter
This uses the model to analyses the sentiment of all the 50,000 tweets and adds it to the larger tweets.csv (located in /data)


Web
------

#### Requirements
* **Bootstrap 4** (Layout + Scrollspy)
* **Jquery** (for bootsrap as well as added functionality on main.js)
* **Plotly-JS** (for bargraphs)

#### Files
* Index.html
		* Basic Bootstrap single column file for arranging data and info etc.
* js/main.js
		* Custom Bargraph function + scrolling change image.
* css/style.css
		* small amount of custom.css (almost all css is straight from boostrap)


[Interactive Graph](https://github.com/tomsaunders98/twittersphere)
----

The interactive bubble chart is hosted on a heroku which is directly connected to a seperate repo ([twittersphere](https://github.com/tomsaunders98/twittersphere)).  

## Share Your Thoughts
I'm on twitter at [@tomandthenews](https://twitter.com/tomandthenews). If you have any questions/suggestions please let me know! 


<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />










