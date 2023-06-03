# Import statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,ConfusionMatrixDisplay
from sklearn import naive_bayes
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
import nltk
import time

import pickle
import joblib

# Support Vector Classifier model
svr_lin = LinearSVC(multi_class='ovr',C=1.0,loss='squared_hinge', dual=False)
tvec = TfidfVectorizer(use_idf=True, strip_accents='ascii')

# function to remove html elements from the reviews
def removeHTML(raw_text):
    clean_HTML = BeautifulSoup(raw_text, 'lxml').get_text()
    return clean_HTML

# function to remove special characters and numbers from the reviews4961
def removeSpecialChar(raw_text):
    clean_SpecialChar = re.sub("[^a-zA-Z]", " ", raw_text)
    return clean_SpecialChar

# function to convert all reviews into lower case
def toLowerCase(raw_text):
    clean_LowerCase = raw_text.lower().split()
    return( " ".join(clean_LowerCase))

def removeStopWords(raw_text):
    #nltk.download('stopwords')
    stops = set(stopwords.words("english"))
    words = [w for w in raw_text if not w in stops]
    return( " ".join(words))

def train_data():
    print("Training.....")
    data = pd.read_csv('amazon_reviews.csv')
    data['sentiment'] = np.where(data['star_rating'] == 5.0, 1, np.where(data['star_rating'] == 4.0, 1, 0))
    # get unique values of product title column
    data["product_title"].unique()

    # choose a particular product for analysis
    prod_hosa = data.loc[data["product_title"]=='Fire HD 7, 7" HD Display, Wi-Fi, 8 GB']
   # print(prod_hosa)

    # #split data-set to train and test
    X = prod_hosa['review_body']
    Y = prod_hosa['sentiment']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=42)

    X_train_cleaned = []
    # print(X_train[])
    # print(X_train.info())

    # To find indices of NaN Values
    # indices = list(np.where(X_train.isna()))
    # print(indices)
    #print(X_train.head())

    # replacing NaN values
    X_train.iloc[23031] = "fine"
    X_train.iloc[14709] = "fine"
    X_train.iloc[21528] = "fine"
    X_train.iloc[23289] = "fine"

    #X_train = X_train.dropna()
    print("X_train NaN found count : ", X_train.isnull().sum())

    #X_test = X_test.dropna()
    print("X_test NaN found count : ", X_test.isnull().sum())

    for val in X_train:

        val = removeHTML(val)
        val = removeSpecialChar(val)
        val = toLowerCase(val)
        removeStopWords(val)
        X_train_cleaned.append(val)

    # X_testing clean set
    X_test_cleaned = []
    for val in X_test:
        val = removeHTML(val)
        val = removeSpecialChar(val)
        val = toLowerCase(val)
        removeStopWords(val)
        X_test_cleaned.append(val)

        # Convert a collection of raw documents to a matrix of TF-IDF features. This is required so as to train the model using features instead of
    # raw strings.
    global tvec
    tvec = TfidfVectorizer(use_idf=True, strip_accents='ascii')

    X_train_tvec = tvec.fit_transform(X_train_cleaned)

    global svr_lin

    saved_model = svr_lin.fit(X_train_tvec, Y_train)



    # #new code starts
    # Save the vectorizer
    vec_file = './vectorizer.pickle'
    pickle.dump(tvec, open(vec_file, 'wb'))

    # Save the model
    mod_file = './classification.model'
    pickle.dump(saved_model, open(mod_file, 'wb'))

    # lr_pickle = pickle.load(open("vectorizer.pickle", 'rb'))
    # review = "three days of use and it broke very disappointed in this product it worked perfectly for exactly three days and could not be resuscitated it was very inexpensive so i did not want to pay half again the price to ship it back for an exchange so the company would do nothing when they sent me an inquiry as to product satisfaction"
    # review2 = "Product is good"
    # demo_review = np.array([review, review2, review2, review])
    #
    # result = lr_pickle.predict(demo_review)
    # print(result)
    #
    # #joblib.dump(trained_model, 'saved_svc_model.pkl')
    #
    # # new code ends

    print("Training Completed!!!!!")
    return True



def validate(predection):
    positive_count = 0
    negative_count = 0

    # counting 1s (positives) and 0s (negatives)
    for i in predection:
        if i == 0:
            negative_count += 1
        else:
            positive_count += 1

    positive_percent = (positive_count/(positive_count+negative_count))*100
    negative_percent = (negative_count / (positive_count + negative_count)) * 100

    sent = ["Positive", "Neutral", "Negative"]

    if positive_percent <= 30:
        print("Overall Sentiment is ", sent[2], ". Predicted Score is ", positive_percent)
        sentiment = sent[2]
        # return sent[2]
    elif 30 < positive_percent <= 65:
        print("Overall Sentiment is ", sent[1], ". Predicted Score is ", positive_percent)
        sentiment = sent[1]
        # return sent[1]
    else:
        print("Overall Sentiment is ",sent[0], ". Predicted Score is ", positive_percent)
        sentiment = sent[0]
        # return sent[0]

    result = {'positive_count' : positive_count, 'negative_count' : negative_count,
              'positive_percent' : round(positive_percent,2), 'negative_percent' : round(negative_percent,2),
              'sentiment' : sentiment
              }
    return result



def testfunc(review):
    # review = "After a month mobile colour is damge"
    review = "three days of use and it broke very disappointed in this product it worked perfectly for exactly three days and could not be resuscitated it was very inexpensive so i did not want to pay half again the price to ship it back for an exchange so the company would do nothing when they sent me an inquiry as to product satisfaction"
    review2 = "Product is good"
    demo_review = np.array([review, review2, review2, review, review])

    global tvec
    review_X_test = tvec.transform(demo_review)
    #print(review_X_test)
    prediction = svr_lin.predict(review_X_test)

    print(prediction)

    # output : [0 1 0] --> prediction as a list

    #validate the prediction to get final value
    overall_prediction = validate(prediction)

    return overall_prediction

import os
def get_sentiment(reviews):


    #review = "three days of use and it broke very disappointed in this product it worked perfectly for exactly three days and could not be resuscitated it was very inexpensive so i did not want to pay half again the price to ship it back for an exchange so the company would do nothing when they sent me an inquiry as to product satisfaction"
    #review2 = "Product is good"

    np_array_review = np.array(reviews)

    # load the vectorizer
    vectorizer_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vectorizer.pickle')
    loaded_vectorizer = pickle.load(open(vectorizer_path, 'rb'))
    review_X_test = loaded_vectorizer.transform(np_array_review)

    # load the model
    model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'saved_svc_model.pkl')
    loaded_model = joblib.load(model_path)

    prediction = loaded_model.predict(review_X_test)
    print(prediction)

    # validate the prediction to get final value
    overall_prediction = validate(prediction)

    return overall_prediction


if __name__ == "__main__":
    st = time.time()

    # train_data()
    # result = get_sentiment("Hello")
    testfunc("review")


    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')






