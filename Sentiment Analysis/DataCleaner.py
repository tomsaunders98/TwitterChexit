#################################################
### Clean Training data before Training Model ###
#################################################



import itertools
import unicodedata
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import string
import datetime
import fasttext
import os


contractions = {
"ain't": "are not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I had",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}
smileys = {
    ":-)": "happy",
    ":-]": "happy",
    ":-3": "happy",
    ":->": "happy",
    "8-)": "happy",
    ":-}": "happy",
    ":)": "happy",
    ";)": "happy",
    ":]": "happy",
    ":3": "happy",
    ":>": "happy",
    "8)": "happy",
    ":}": "happy",
    ":o)": "happy",
    ":c)": "happy",
    ":^)": "happy",
    "=]": "happy",
    "=)": "happy",
    ":-))": "happy",
    ":‑D": "happy",
    "8‑D": "happy",
    "x‑D": "happy",
    "X‑D": "happy",
    ":D": "happy",
    "8D": "happy",
    "xD": "happy",
    "XD": "happy",
    ":‑(": "sad",
    ":‑c": "sad",
    ":‑<": "sad",
    ":‑[": "sad",
    ":(": "sad",
    ":c": "sad",
    ":<": "sad",
    ":[": "sad",
    ":-||": "sad",
    ">:[": "sad",
    ":{": "sad",
    ":@": "sad",
    ">:(": "sad",
    ":'‑(": "sad",
    ":'(": "sad",
    ":‑P": "playful",
    "X‑P": "playful",
    "x‑p": "playful",
    ":‑p": "playful",
    ":‑Þ": "playful",
    ":‑þ": "playful",
    ":‑b": "playful",
    ":P": "playful",
    "XP": "playful",
    "xp": "playful",
    ":p": "playful",
    ":Þ": "playful",
    ":þ": "playful",
    ":b": "playful",
    "<3": "love"
}

def clean_accents(text):
    # first, normalize strings:
    nfkd_str = unicodedata.normalize('NFKD', text)

    # Keep chars that has no other char combined (i.e. accents chars)
    with_out_accents = u"".join([c for c in nfkd_str if not unicodedata.combining(c)])
    return with_out_accents

def removedict(text, dict):
    text = text.replace("’", "'")
    pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in dict.keys()) + r')(?!\w)')
    return pattern.sub(lambda x: dict[x.group()], text)

def spell(text):
    return ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))




def removesmiley(text, dict):
    text = (re.sub('[\U0001F602-\U0001F64F]', lambda m: unicodedata.name(m.group()), text)).lower()
    text = removedict(text, smileys)
    return text


def detweet(text):
    #remove html
    text = text.replace("#", "")
    text = text.replace('\u2044', ' or ')
    text = BeautifulSoup(text,features="html.parser").get_text()
    text = text.replace('\x92', "'")

    #remove hashtags (but just hashtags, they can be quite informative about sentiment)

    #remove mentions
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)", "", text).split(" "))
    # remove web adress
    text = ' '.join(re.sub("(\w+:\/\/\S+)", " ", text).split())
    return text


def removepunctuation(text):
    #remove punctuation
    return text.translate(str.maketrans('', '', string.punctuation))

def removestop(text):
    stops = set(stopwords.words("english-sent"))
    filtered_words = ' '.join([word for word in text.split() if word not in stops])
    return filtered_words

def correct(text):
    #1 remove capitals
    text = text.lower()
    # 2 accents
    text = clean_accents(text)
    #3 remove links/hastags/mentions/html characters
    text = detweet(text)
    #4 remove smileys
    text = removesmiley(text, smileys)
    #5 remove contractions
    text = removedict(text, contractions)
    #6 remove punctuation
    text = removepunctuation(text)
    #7 correct spellings
    text = spell(text)
    #8 remove stopwords
    text = removestop(text)
    #9 remove any non ascii characters
    text = re.sub(r'[^\x00-\x7f]', r'', text)
    return text

def formattweet(row):
    cur_row = []
    # Prefix the index-ed label with __label__
    label = "__label__" + row[4]
    cur_row.append(label)
    cur_row.extend(word_tokenize(correct(row[2].lower())))
    return cur_row

def preprocess(input_file, output_file, keep=1):
    i=0
    with open(output_file, 'w') as csvoutfile:
        csv_writer = csv.writer(csvoutfile, delimiter=' ', lineterminator='\n')
        with open(input_file, 'r', newline='') as csvinfile: #,encoding='latin1'
            csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if row[4]!="MIXED" and row[4].upper() in ['POSITIVE','NEGATIVE','NEUTRAL'] and row[2]!='':
                    row_output = formattweet(row)
                    csv_writer.writerow(row_output )
                i=i+1
                if i%10000 ==0:
                    print(i)


def upsampling(input_file, output_file, ratio_upsampling=1):
    # Create a file with equal number of tweets for each label
    #    input_file: path to file
    #    output_file: path to the output file
    #    ratio_upsampling: ratio of each minority classes vs majority one. 1 mean there will be as much of each class than there is for the majority class

    i = 0
    counts = {}
    dict_data_by_label = {}

    # GET LABEL LIST AND GET DATA PER LABEL
    with open(input_file, 'r', newline='') as csvinfile:
        csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            counts[row[0].split()[0]] = counts.get(row[0].split()[0], 0) + 1
            if not row[0].split()[0] in dict_data_by_label:
                dict_data_by_label[row[0].split()[0]] = [row[0]]
            else:
                dict_data_by_label[row[0].split()[0]].append(row[0])
            i = i + 1
            if i % 10000 == 0:
                print("read" + str(i))

    # FIND MAJORITY CLASS
    majority_class = ""
    count_majority_class = 0
    for item in dict_data_by_label:
        if len(dict_data_by_label[item]) > count_majority_class:
            majority_class = item
            count_majority_class = len(dict_data_by_label[item])

            # UPSAMPLE MINORITY CLASS
    data_upsampled = []
    for item in dict_data_by_label:
        data_upsampled.extend(dict_data_by_label[item])
        if item != majority_class:
            items_added = 0
            items_to_add = count_majority_class - len(dict_data_by_label[item])
            while items_added < items_to_add:
                data_upsampled.extend(
                    dict_data_by_label[item][:max(0, min(items_to_add - items_added, len(dict_data_by_label[item])))])
                items_added = items_added + max(0, min(items_to_add - items_added, len(dict_data_by_label[item])))

    # WRITE ALL
    i = 0

    with open(output_file, 'w') as txtoutfile:
        for row in data_upsampled:
            txtoutfile.write(row + '\n')
            i = i + 1
            if i % 10000 == 0:
                print("writer" + str(i))

training_data_path ='C:\\Users\\Tom\\PycharmProjects\\SentimentAnalysis\\uptweets.train'
validation_data_path ='C:\\Users\\Tom\\PycharmProjects\\SentimentAnalysis\\tweets.validation'
model_path ='C:\\Users\\Tom\\PycharmProjects\\SentimentAnalysis\\'
model_name="model-en"

def train():
    print('Training start')
    try:
        hyper_params = {"lr": 0.01,
                        "epoch": 20,
                        "wordNgrams": 2,
                        "dim": 20}

        print(str(datetime.datetime.now()) + ' START=>' + str(hyper_params))

        # Train the model.
        model = fasttext.train_supervised(input=training_data_path, **hyper_params)
        print("Model trained with the hyperparameter \n {}".format(hyper_params))

        # CHECK PERFORMANCE
        print(str(datetime.datetime.now()) + 'Training complete.' + str(hyper_params))

        result = model.test(training_data_path)
        validation = model.test(validation_data_path)

        # DISPLAY ACCURACY OF TRAINED MODEL
        text_line = str(hyper_params) + ",accuracy:" + str(result[1]) + ",validation:" + str(validation[1]) + '\n'
        print(text_line)

        # quantize a model to reduce the memory usage
        model.quantize(input=training_data_path, qnorm=True, retrain=True, cutoff=100000)
        print("Model is quantized!!")
        model.save_model(os.path.join(model_path, model_name + ".ftz"))

        ##########################################################################
        #
        #  TESTING PART
        #
        ##########################################################################
        model.predict(['why not'], k=3)
        model.predict(['this player is so bad'], k=1)

    except Exception as e:
        print('Exception during training: ' + str(e))


# Train your model.
#train()
#upsampling('tweets.train', 'uptweets.train')

# Preparing the training dataset
#preprocess('betsentiment-EN-tweets-sentiment-teams.csv', 'tweets.train')

# Preparing the validation dataset
#preprocess('betsentiment-EN-tweets-sentiment-players.csv', 'tweets.validation')














#To Do
#1 accents (any of that stuff) done
#2 contractions done
#3 misspellings done
#4 lower case done
#5 emojis done
#6 emoticons done
#7 stopwords done
# escaping html done
# links done
# punctuation done
# removal of hashtags/mentions done
# formatting
#(not neccesarily in thatfro