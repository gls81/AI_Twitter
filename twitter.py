import csv
import random
import nltk
import re

from happyfuntokenizing import Tokenizer

from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.corpus import names
 
 
basetrain = '/Users/gls/Documents/Uni/AI For Applications/Assignment/'
trainfile = 'tweeti-b-gold_standard_v2'
testfile  = 'tweeti-b.dev.dist'
tweetsfile = 'tweets'
train_tweets = 'tweeti-b-gold_standard_tweets'
dev_tweets = 'tweeti-b.dev.dist_tweets'
postive_list = 'positive.txt'
negative_list = 'negative.txt'
ext = '.tsv'
emoticons = """:-) :) :o) :] :3 :c) :> =] 8) =) :} :^) 
             :D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D
             :-D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D
             >:[ :-( :(  :-c :c :-< :< :-[ :[ :{ ;(
             :-|| :@ >:( :'-( :'( :'-) :') D:< D: D8 D; D= DX v.v D-':
             >:O :-O :O :-o :o 8-0 O_O o-o O_o o_O o_o O-O
             >:P :-P :P X-P x-p xp XP :-p :p =p :-b :b d:""".split()
emo_pattern = "|".join(map(re.escape, emoticons))

class semeval():
    tweets_dict = {}
    dev_tweets = {}
    train_tweets = {}

    def __init__(self):
        self.negative = []
        self.positive = []
        self.posAndNegList()
        self.readRawData()
        self.shuffleData()
        self.splitData()
        self.trainClassifier()
        return

    def readRawData(self):
        """Read in the tweets """
        print 'reading'
        self.tweetDict={}
        cnt=0
        with open(basetrain + train_tweets + ext,'rb') as tsvin:
            for line in csv.reader(tsvin, delimiter='\t'):
                cnt+=1
                #if cnt==5:
                    #break
                tweet_number = long(line[0])
                tweet_text = line[2].rstrip("\n\r")
                self.tweetDict[tweet_number]=tweet_text

        self.tweetFullList=[]

        with open(basetrain + trainfile + ext,'rb') as tsvin:
            for line in csv.reader(tsvin, delimiter='\t'):
                tweet_number = long(line[0])

                if self.tweetDict[tweet_number] != "Not Available":
                    tweet_class = line[2].rstrip("\n\r")

                    #Should split this out maybe pass in option the have another class tweet feature extraction/processing
                    
                    tup=()
                    tup=self.defineFeatures(self.tweetDict[tweet_number],tweet_class)
                    #tup2=()
                    #tup2=self.posSearch(self.tweetDict[tweet_number],tweet_class)
                    #tup3=()
                    #tup3=self.negSearch(self.tweetDict[tweet_number],tweet_class)
                    #print cnt
                    cnt -= 1
                    #dct={}
                    #dct['tweet']=tweet_text
                    #tup=()
                    #tup=(dct,tweet_class)

                    self.tweetFullList.append(tup)
                    #self.tweetFullList.append(tup2)
                    #self.tweetFullList.append(tup3)
        #print self.tweetFullList
        return

    def createTweetList(self):
        print 'creating tweet list...'
        self.nameList=[]
        for name in self.males:
            tup=()
            tup=(name,'male')
            self.nameList.append(tup)

        for name in self.females:
            tup=()
            tup=(name,'female')
            self.nameList.append(tup)
             
        #print self.nameList
        return

    def splitData(self):
        print 'splitting'
        tot=len(self.tweetFullList)
        self.trainData = self.tweetFullList[1:int(0.8*tot)]
        self.devData = self.tweetFullList[int(0.8*tot):int(0.9*tot)]
        self.testData = self.tweetFullList[int(0.9*tot):int(tot)]
        #print self.trainData
        return

    def shuffleData(self):
        print 'shuffling'
        random.shuffle(self.tweetFullList)
        return

 
    def posAndNegList(self):
        with open(postive_list, 'r') as f:
            for line in csv.reader(f, delimiter='\n'):
                self.positive += line
        with open(negative_list, 'r') as f:
            for line in csv.reader(f, delimiter='\n'):
                self.negative += line
              
        return
     
    def trainClassifier(self):
        print 'training classifier.'
        self.classifier = nltk.NaiveBayesClassifier.train(self.trainData)
        print nltk.classify.accuracy(self.classifier, self.testData)
        self.classifier.show_most_informative_features(10)
        return
     
    def fake_analyze_tweet( self, tweet_text):
        """This DOES NOT analyze tweets, it just returns one value. You replacement function should do more"""
        if self.mode == "random":
            return random.choice(["positive", "negative", "objective"])
        else:
            return self.mode

    def defineFeatures(self, tweet_text, tweet_class):
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

    def removeStopWords(self, words):
        #if self.options['stop'] == 1:
        stopwords = nltk.corpus.stopwords.words('english')
        words = [w for w in words if w.lower() not in stopwords]
        return words
    
        
 
if __name__ == '__main__':
     app = semeval()
     #app.run_semeval()
 
