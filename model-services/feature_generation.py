import pika
from homer.analyzer import Article
from homer.cmdline_printer import ArticlePrinter
import textstat
import nltk

nltk.download('punkt')
nltk.download('cmudict')
nltk.download('stopwords')

columns = [
    'AccessionID',
    'reading_time', 
    'flesch_reading_score', 
    'dale_chall_readability_score',
    'total_paragraphs',
    'avg_sentences_per_para',
    'len_of_longest_paragraph',
    'total_sentences',
    'avg_words_per_sentence',
    'len_of_longest_sentence',
    'total_words',
    'compulsive_hedgers',
    'intensifiers',
    'and_frequency',
    'vague_words_count',
    'vague_words_frequency',
    'polysyllab_count',
    'polysyllab_frequency'
]

def generate_features(text):
    article = Article('Article name', 'Author', text)

    reading_time = article.reading_time
    flesch_reading_score = textstat.flesch_reading_ease(text)
    dale_chall_readability_score = round(textstat.dale_chall_readability_score(text), 1)
    total_paragraphs = article.total_paragraphs
    avg_sentences_per_para = article.avg_sentences_per_para
    # standard deviation
    len_of_longest_paragraph = article.len_of_longest_paragraph
    total_sentences = article.total_sentences
    avg_words_per_sentence = article.avg_words_per_sentence
    len_of_longest_sentence = article.len_of_longest_sentence
    total_words = article.total_words
    compulsive_hedgers = len(article.get_compulsive_hedgers())
    intensifiers = len(article.get_intensifiers())
    and_frequency = float(article.get_and_frequency().replace(" %",""))
    vague_words_count = len(article.get_vague_words())
    vague_words_frequency = vague_words_count/total_words
    polysyllab_count = textstat.polysyllabcount(text)
    polysyllab_frequency = polysyllab_count/total_words

    return (
        reading_time, 
        flesch_reading_score, 
        dale_chall_readability_score, 
        total_paragraphs, 
        avg_sentences_per_para, 
        len_of_longest_paragraph,
        total_sentences,
        avg_words_per_sentence,
        len_of_longest_sentence,
        total_words,
        compulsive_hedgers,
        intensifiers,
        and_frequency,
        vague_words_count,
        vague_words_frequency,
        polysyllab_count,
        polysyllab_frequency
    )