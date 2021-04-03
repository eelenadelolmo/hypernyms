import os
import shutil
from rake_nltk import Rake
from rake_nltk import Metric


dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/rake/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)
docs = os.listdir(dir_all)

# Rake default execution
# metric for ranking == DEGREE_TO_FREQUENCY_RATIO
# Using stopwords for english from NLTK, and all puntuation characters
r = Rake()
folder = 'rake_degreeFreqRatio/'
os.makedirs(dir_kw + folder)
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        r.extract_keywords_from_text(texto)
        keywords = r.get_ranked_phrases()
    with open(dir_kw + folder + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords:
            f_w.write('- ' + keyword + '\n')

## Rake controlling the number of words in keywords
r = Rake(max_length=4)
folder = 'rake_degreeFreqRatio_length/'
os.makedirs(dir_kw + folder)
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        r.extract_keywords_from_text(texto)
        keywords = r.get_ranked_phrases()
    with open(dir_kw + folder + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords:
            f_w.write('- ' + keyword + '\n')

## Rake with the metric for ranking = WORD_DEGREE
r = Rake(ranking_metric=Metric.WORD_DEGREE, max_length=4)
folder = 'rake_metric_wordDegree_length/'
os.makedirs(dir_kw + folder)
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        r.extract_keywords_from_text(texto)
        keywords = r.get_ranked_phrases()
    with open(dir_kw + folder + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords:
            f_w.write('- ' + keyword + '\n')

## Rake with the metric for ranking = WORD_FREQUENCY
r = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=4)
folder = 'rake_metric_wordFreq_length/'
os.makedirs(dir_kw + folder)
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        r.extract_keywords_from_text(texto)
        keywords = r.get_ranked_phrases()
    with open(dir_kw + folder + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords:
            f_w.write('- ' + keyword + '\n')
