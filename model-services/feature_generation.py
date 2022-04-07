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

    total_words = article.total_words
    compulsive_hedgers = len(article.get_compulsive_hedgers())
    intensifiers = len(article.get_intensifiers())
    and_frequency = float(article.get_and_frequency().replace(" %",""))
    vague_words_count = len(article.get_vague_words())
    vague_words_frequency = vague_words_count/total_words
    polysyllab_count = textstat.polysyllabcount(text)

    raw_feature = np.array([polysyllab_count, compulsive_hedgers, vague_words_frequency, and_frequency, intensifiers])
    normalized = (raw_feature - features_means) / features_stds

    return normalized
