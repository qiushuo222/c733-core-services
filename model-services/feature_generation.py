import os
import json

import pika
import numpy as np
from homer.analyzer import Article
from homer.cmdline_printer import ArticlePrinter
import textstat
import nltk

nltk.download('punkt')
nltk.download('cmudict')
nltk.download('stopwords')

features_stds = np.array(json.loads(os.environ["FEATURE_STDS"]))
features_means = np.array(json.loads(os.environ["FEATURE_MEANS"]))

def generate_features(text):
    article = Article('Article name', 'Author', text)

    flesch_reading_score = textstat.flesch_reading_ease(text)
    dale_chall_readability_score = round(textstat.dale_chall_readability_score(text), 1)
    # standard deviation
    avg_words_per_sentence = article.avg_words_per_sentence
    total_words = article.total_words
    compulsive_hedgers = len(article.get_compulsive_hedgers())
    polysyllab_count = textstat.polysyllabcount(text)
    polysyllab_frequency = polysyllab_count / total_words

    raw_feature = np.array([compulsive_hedgers, polysyllab_frequency, avg_words_per_sentence, dale_chall_readability_score, flesch_reading_score])
    normalized = (raw_feature - features_means) / features_stds

    return normalized
