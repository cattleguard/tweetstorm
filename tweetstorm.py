#!/usr/bin/python3

# Notes:
#   *   Will break on storms requiring more than double digits.
#   *   Using index() to figure out the number of the tweet means that if strings perfectly repeat the first matched index will be returned and numbering will be off.

import re
from nltk.tokenize import sent_tokenize
import nltk
import sys
import argparse

# argparse stuff

parser = argparse.ArgumentParser(description='tweetstorm.py, because sometimes your thoughts are bigger than 240 characters')
parser.add_argument("--text", help="text to tweetstorm")
args = parser.parse_args()

# Download punkt tokenizer
nltk.download('punkt', quiet = True)
paragraph = ""
max_tweet_len = 240-7
if args.text is not None:
    paragraph = args.text
else:
    paragraph = str(sys.stdin.read())

# Just some cleaning stuff.
paragraph = re.sub('[\n]','', paragraph)
paragraph = re.sub(r'[\s]{2,}',' ', paragraph)

# Tokenize into sentences
paragraph = sent_tokenize(paragraph)

n_tweets_needed = 0
tweet_list = []
tweet = str()

sentence_list = []

# Chunk the long sentences.
for sentence in paragraph:
    if len(sentence) > (max_tweet_len -3):
        h = [ sentence[i:i+(max_tweet_len-3)] for i in range(0, len(sentence), (max_tweet_len-3)) ]
        for x in h:
            if h.index(x) < len(h)-1:
                sentence_list.append(x+"...")
            else:
                sentence_list.append(x)
    else:
        sentence_list.append(sentence)

# Combine short sentences.
for sentence in sentence_list:
    if len(tweet + " " + sentence) < max_tweet_len:
        tweet = tweet + " " + sentence
    else:
        tweet_list.append(tweet)
        tweet = sentence
        n_tweets_needed += 1

# Flush if not empty
if len(tweet) != 0:    
    tweet_list.append(tweet)

for t in tweet_list:
    the_tweet = t.strip()+"("+str(tweet_list.index(t)+1)+"/"+str(n_tweets_needed+1)+")"
    print(the_tweet+"\n")
