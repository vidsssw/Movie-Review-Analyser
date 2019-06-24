
from typing import List, Any
import nltk
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
import pickle
import pandas as pd
import numpy as np


## Vote Classifier Class - This class helps decide the confidence by determining the mode of votes of a review

class VoteClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers=classifiers

    def classify(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self,features):
        votes = []

        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        no_of_times=votes.count(mode(votes))
        conf=no_of_times / len(votes)
        return conf

## create our document that contains reviews and their category


positive = open("positive.txt", "r").read()
negative = open("negative.txt", "r").read()

documents = []

for r in positive.split('\n'):
    documents.append((r, "pos"))

for r in negative.split('\n'):
    documents.append((r, "neg"))

## create our word features

all_words = []

positive_words = word_tokenize(positive)
negative_words = word_tokenize(negative)

stop_words = set(stopwords.words("english"))

for w in positive_words:
    if (w not in stop_words) and (w != ',') and (w != '.') and (w != '!'):
        p=nltk.pos_tag(w)
        for k in p:
            if k[1][0] == "J":
                all_words.append(k[0].lower())


for w in negative_words:
    if (w not in stop_words) and (w != ',') and (w != '.') and (w != '!'):
        p = nltk.pos_tag(w)
        for k in p:
            if k[1][0] == "J":
                all_words.append(k[0].lower())




all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:1300]


## create function that checks for feature words in a review
## feature array will contain the feature word and whether it is present or not in this review

def findfeatures(document):
    features = {}
    words = word_tokenize(document)
    for w in word_features:
        features[w] = (w in words)
    return features


## create a feature set for our document which will be used as train and test data

featuresets = [(findfeatures(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)

## distribute into testing and training data

training_data = featuresets[:1300]
testing_data = featuresets[1300:]

## Using Naive Baye's classifier from nltk

'''
classifier_NB=open("NBClassifier.pickle","rb")
NB_classifier=pickle.load(classifier_NB)
classifier_NB.close()
'''
classifier_NB = nltk.NaiveBayesClassifier.train(training_data)
#print(nltk.classify.accuracy(classifier_NB, testing_data) * 100)


## Using MultinomalNB , BernoulliNB from sklearn

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_data)
#print(nltk.classify.accuracy(MNB_classifier, testing_data) * 100)
'''
classifier_MNB=open("MNBClassifier.pickle","rb")
MNB_classifier=pickle.load(classifier_MNB)
classifier_MNB.close()
'''
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_data)
#print(nltk.classify.accuracy(BNB_classifier, testing_data) * 100)
'''
classifier_BNB=open("BNBClassifier.pickle","rb")
BNB_classifier=pickle.load(classifier_BNB)
classifier_BNB.close()
'''
## Using LogisticRegression and SDG Regression from sklearn

LR_classifier = SklearnClassifier(LogisticRegression())
LR_classifier.train(training_data)
#print(nltk.classify.accuracy(LR_classifier, testing_data) * 100)
''' 
classifier_LR=open("LRClassifier.pickle","rb+")
LR_classifier=pickle.load(classifier_LR)
classifier_LR.close()
'''
SGD_classifier = SklearnClassifier(SGDClassifier())
SGD_classifier.train(training_data)
#print(nltk.classify.accuracy(SGD_classifier, testing_data) * 100)
'''
classifier_SGD=open("SGDClassifier.pickle","rb")
SGD_classifier=pickle.load(classifier_SGD)
classifier_SGD.close()

'''
## Using SVC, LinearSVC , NuSVC from sklearn

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_data)
#print(nltk.classify.accuracy(SVC_classifier, testing_data) * 100)
'''
classifier_SVC=open("SVCClassifier.pickle","rb")
SVC_classifier=pickle.load(classifier_SVC)
classifier_SVC.close()
'''
LSVC_classifier = SklearnClassifier(LinearSVC())
LSVC_classifier.train(training_data)
#print(nltk.classify.accuracy(LSVC_classifier, testing_data) * 100)
'''
classifier_LSVC=open("LSVCClassifier.pickle","rb")
LSVC_classifier=pickle.load(classifier_LSVC)
classifier_LSVC.close()
'''
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_data)
#print(nltk.classify.accuracy(NuSVC_classifier, testing_data) * 100)
'''
classifier_NuSVC=open("NuSVCClassifier.pickle","rb")
NuSVC_classifier=pickle.load(classifier_NuSVC)
classifier_NuSVC.close()
'''

## Create object of VoteClassifier class and pass list of Classifiers

voted_classifier = VoteClassifier(LSVC_classifier,classifier_NB,LR_classifier,MNB_classifier,BNB_classifier)


def sentiment(text):
    feats=findfeatures(text)

    return(voted_classifier.classify(feats))

'''
print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_data)) * 100)

print("The review is:" + voted_classifier.classify(testing_data[0][0]))

print("The confidence score is:" + voted_classifier.confidence(training_data[0][0]))
'''
