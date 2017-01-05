import os, pickle, openpyxl
from statistics import mode
from progress.bar import IncrementalBar
# Parsing Algorithms
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer
# returns the most appropriate label for the given featureset -->
from nltk.classify import ClassifierI
# Training Algorithms
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from pymongo import MongoClient
from lib import helper

KEYWORD1 = input()
KEYWORD2 = input()
SINCE   = input()
UNTIL   = input()
DBName  = input()
COUNTRY = input()
CACHE   = bool(input())
PORT    = int(input())

class Classifier(ClassifierI):
    def __init__(self, *args):
        self.__classifiers = list(args)
    def push(self, clf):
        self.__classifiers += [clf]
    # extend the functionality of 'ClassifierI.classify()' function
    def classify(self, features):
        votes = []
        for c in self.__classifiers:
            v = c.classify(features)
            votes.append(v)
        winner = mode(votes)
        chosen_winner = votes.count(winner)
        confidence = round(chosen_winner/len(votes)*100, 2)
        return winner, confidence

def write_header(worksheet, headers):
    for k in range(1, len(headers)+1):
        worksheet.cell(row=1, column=k, value=headers[k-1])
        worksheet.cell(row=1, column=k).font = openpyxl.styles.Font(bold=True)
    return 2

def sentiment(text, featuring_words):
    words = tokenizer.tokenize(text)
    words = [w.lower() for w in words if w.lower() not in stop_words]
    featureset = {}
    for w in featuring_words:
        featureset[w] = (w in words)
    return clfs.classify(featureset)

if __name__ == '__main__':
    tokenizer  = TweetTokenizer()
    stop_words = stopwords.words('english')
    # -----------------------------------------------------------
    print('Loading Trained Classifiers ...')
    classifiers = ['MultinomialNB','BernoulliNB',
                   'LogisticRegression','SGDClassifier',
                   'SVC','NuSVC','LinearSVC' ]
    clfs = Classifier()
    for clf in classifiers:
        f = open('algos/'+clf+'classifier.pkl','rb')
        classifier = pickle.load(f)
        clfs.push(classifier)
        f.close()
    # -----------------------------------------------------------
    print('Loading featuring words (predictors) ...')
    f = open('algos/featuring_words.pkl', 'rb')
    featuring_words = pickle.load(f)
    f.close()
    # -----------------------------------------------------------
    print('Analysing sentiments and confidence ...')
    client = MongoClient(port=PORT)
    db = client[DBName]
    source = db.metadata.find()[0]['source']
    tweets = db.tweets.find()
    # -----------------------------------------------------------
    var  = helper.get_variables('config/variables.yml')
    headers  = var['user'] + var['place']
    headers += var['tweet'] + var['author'] + var['source']
    headers += ['confidence', 'category']
    # -----------------------------------------------------------
    bar = IncrementalBar('Processing ', max=tweets.count())
    # -----------------------------------------------------------
    workbook  = openpyxl.workbook.Workbook()
    worksheet = workbook.active
    worksheet.title = 'DATA'
    row = write_header(worksheet, headers)
    # -----------------------------------------------------------
    for tweet in tweets:
        user = db.users.find({ 'user_id' : { '$eq' : tweet['user_id'] }})
        user = user[0]
        category, confidence = sentiment(tweet['text'], featuring_words)
        col = 1
        for colname in headers:
            if colname in var['user'] or colname in var['place']:
                worksheet.cell(row=row, column=col, value=str(user[colname]))
            elif colname in var['tweet'] or colname in var['author'] or colname in var['source']:
                worksheet.cell(row=row, column=col, value=str(tweet[colname]))
            elif colname=='confidence':
                worksheet.cell(row=row, column=col, value=confidence)
            elif colname=='category':
                worksheet.cell(row=row, column=col, value=category)
            col += 1
        row += 1
        bar.next()
    # -----------------------------------------------------------
    outpath = 'app/output/'+DBName
    if not os.path.exists(outpath) and not os.path.isdir(outpath):
        print('Creating output folder ...')
        os.mkdir(outpath)
    workbook.save(outpath+'/'+DBName+'.xlsx')
    print(' Done.\nClassification Completed !!!')
