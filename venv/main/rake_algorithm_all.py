import string
from rake_nltk import Rake
from rake_nltk import Metric
from nltk.corpus import stopwords

all = 'corpus/Medical/txt_all.txt'

# Rake default exacution
# metric for ranking == DEGREE_TO_FREQUENCY_RATIO
# Using stopwords for english from NLTK, and all puntuation characters
r = Rake(stopwords=stopwords.words('english'), punctuations=string.punctuation + '•')
with open(all) as f:
    texto = f.read()
    r.extract_keywords_from_text(texto)
    keywords = r.get_ranked_phrases()

with open('corpus/Medical/txt_all_rake_degreeFreqRatio.txt', 'w') as f_w:
    for keyword in keywords:
        f_w.write('-' + keyword + '\n')

# controlling the number of words in keywords
# metric for ranking == DEGREE_TO_FREQUENCY_RATIO
r = Rake(stopwords=stopwords.words('english'), punctuations=string.punctuation + '•', max_length=4)
with open(all) as f:
    texto = f.read()
    r.extract_keywords_from_text(texto)
    keywords = r.get_ranked_phrases()

with open('corpus/Medical/txt_all_rake_degreeFreqRatio_length.txt', 'w') as f_w:
    for keyword in keywords:
        f_w.write('-' + keyword + '\n')




## Rake with the metric for ranking = WORD_DEGREE
r = Rake(stopwords=stopwords.words('english'), punctuations=string.punctuation + '•', ranking_metric=Metric.WORD_DEGREE, max_length=4)
with open(all) as f:
    texto = f.read()
    r.extract_keywords_from_text(texto)
    keywords = r.get_ranked_phrases()

with open('corpus/Medical/txt_all_rake_wordDegree_length.txt', 'w') as f_w:
    for keyword in keywords:
        f_w.write('-' + keyword + '\n')




## Rake with the metric for ranking = WORD_FREQUENCY
r = Rake(stopwords=stopwords.words('english'), punctuations=string.punctuation + '•', ranking_metric=Metric.WORD_FREQUENCY, max_length=4)
with open(all) as f:
    texto = f.read()
    r.extract_keywords_from_text(texto)
    keywords = r.get_ranked_phrases()

with open('corpus/Medical/txt_all_rake_wordFreq_length.txt', 'w') as f_w:
    for keyword in keywords:
        f_w.write('-' + keyword + '\n')

