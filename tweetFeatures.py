import csv
import random
import nltk
import re

from happyfuntokenizing import Tokenizer
from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize






#Create string of emoticons 
emoticons = """:-) :) :o) :] :3 :c) :> =] 8) =) :} :^) 
             :D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D
             :-D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D
             >:[ :-( :(  :-c :c :-< :< :-[ :[ :{ ;(
             :-|| :@ >:( :'-( :'( :'-) :') D:< D: D8 D; D= DX v.v D-':
             >:O :-O :O :-o :o 8-0 O_O o-o O_o o_O o_o O-O
             >:P :-P :P X-P x-p xp XP :-p :p =p :-b :b d:""".split()
emo_pattern = "|".join(map(re.escape, emoticons))
postive_list = 'positive.txt'
negative_list = 'negative.txt'
baseDir = '/Users/gls/Documents/Uni/AI For Applications/Assignment/'


class tweetFeatures():

    def __init__(self):

        return

    def posAndNegList(self):
        with open(postive_list, 'r') as f:
            for line in csv.reader(f, delimiter='\n'):
                self.positive += line
        with open(negative_list, 'r') as f:
            for line in csv.reader(f, delimiter='\n'):
                self.negative += line
              
        return

    def emoticonSearch(self, tweet_text, tweet_class):
        """Call other methods from here to define the features of the tweet"""
        #remove stop words
        #tokenize
        #tweet_text = self.removeStopWords(tweet_text)
        #print tweet_text
        #t =  Tokenizer()
        #tweet_tokens = t.tokenize(tweet_text)
        dic = {}
        tup = ()
        dic['emoticon']=' '.join(re.findall(emo_pattern, tweet_text))          
        tup=(dic,tweet_class)

        return tup

    def posSearch(self, tweet_text, tweet_class):
        dic = {}
        tup = ()
        cnt = 0
        for w in self.positive:
            w = re.escape(w)
            regex = re.compile(r'%s'%w)
            if re.findall(regex, tweet_text):
                cnt += 1
        dic['pos_count']= cnt
        tup=(dic,tweet_class)
        return tup

    def negSearch(self, tweet_text, tweet_class):
        dic = {}
        tup = ()
        cnt = 0
        for w in self.negative:
            w = re.escape(w)
            regex = re.compile(r'%s'%w)
            if re.findall(regex, tweet_text):
                cnt += 1
        dic['neg_count']= cnt
        tup=(dic,tweet_class)
        return tup
