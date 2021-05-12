import numpy as np
import pandas as pd
from pprint import pprint
import warnings
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.preprocessing import FunctionTransformer

from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline

from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import f1_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import mlflow.sklearn
import mlflow

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    df = pd.read_excel("/Users/manon/Projet/IA_Processing/labels-voix-ca-lot-6-reduit.xlsx")
    df = df[['text', 'category', 'is_project']]
    df_s = df.groupby(['text', 'category'])['is_project'].first().unstack(-1)
    df_s = (~df_s.isna()).astype(int)

       # Les noms des colonnes cibles
    category_cols = [
              'Credit_vehicule', 'Bilan_suivi_relationnel',
             '_pargne_terme',
             #'Credit_travaux',
             'Entree_en_relation_Conquetes',
             'Point_d_attention_risques', 'Reclamation_Insatisfaction_client',
             'Credit_conso',
             #'_venements_de_vie','Credit_agri_pro',
              '_pargne_disponible',
              'Non_specifie_Credit_Assurance_Epargne_', 'Assurance_de_Biens',
             'Assurance_de_Personnes', 'BAQ_Services_Bancaires',
              'Credit_habitat',  'Projet_exceptionnel_']

    df_s = df_s.reset_index()
    df_s.text = df_s.text.astype(str)
    transformer = FunctionTransformer()
    transformer.transform(df_s['text'])
    # Chargement stopwords français
    stop_words = stopwords.words('french')

    # Initialize stemmer, which will take words and convert words to their "stem," e.g. Playing-> Play
    ps = PorterStemmer()


# Enlever les charactères nons alphabétiques, espaces et convertir toutes les lettres en minuscules
# References: https://www.analyticsvidhya.com/blog/2019/04/predicting-movie-genres-nlp-multi-label-classification/
    def clean_text(txt):
        txt = txt.lower()  # lowercase
        txt = re.sub("[^a-zA-Z]", " ", txt)  # Remove everything except alphabetical characters
        txt = word_tokenize(txt)  # tokenize (split into list and remove whitespace)

    # initialize list to store clean text
        clean_text = ""

    # iterate over each word
        for w in txt:
        # remove stopwords
            if w not in stop_words:
            # stem=ps.stem(w) #stem
                stem = w
                clean_text += stem + " "
        return clean_text


    text_new = []  # declare a list to hold new movies

    for cell in df_s['text']:
        txt = clean_text(cell)
        text_new.append(txt)

    # add new info column to the dataframe
    df_s['text'] = text_new

    # prepare training data
    X_train, X_test, y_train, y_test = train_test_split(df_s['text'], df_s[category_cols], random_state=0)




def eval_metrics(y_test, predict_decision_tree):
    f1 = f1_score(y_test, predict_decision_tree, average='macro')
    recall = recall_score(y_test, predict_decision_tree, average='macro')
    precision = precision_score(y_test, predict_decision_tree, average='macro')
    return f1, recall, precision

# enable autologging
mlflow.sklearn.autolog()


# train a model
pipe = Pipeline([
    ('countVectorier', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    # Pour gérer les cas multi-label
    ('multiclass', MultiOutputClassifier(
    # Le solveur par defaut est lent dans le cas sparse
       estimator=DecisionTreeClassifier(random_state=0)
    ))
])

with mlflow.start_run() as run:
    mlflow.set_tag("release.version", "1.0.0")
    pipe.fit(X_train, y_train)

    predict_decision_tree = pipe.predict(X_test)

    (f1, recall, precision) =  eval_metrics(y_test, predict_decision_tree)

    print("  Precision: %s" % precision)
    print("  Recall: %s" % recall)
    print("  F1-score: %s" % f1)

    mlflow.log_metric("precision", precision)
    mlflow.log_metric("F1-score", f1)
    mlflow.log_metric("recall", recall)






