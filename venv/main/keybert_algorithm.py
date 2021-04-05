from keybert import KeyBERT
import shutil
import os

kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')

dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/keybert/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)
docs = os.listdir(dir_all)



os.makedirs(dir_kw + 'keybert/')
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        keywords = kw_extractor.extract_keywords(texto, keyphrase_ngram_range=(1,15), stop_words='english', top_n=10)
    with open(dir_kw + 'keybert/' + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords[0][0].split():
            f_w.write('-' + keyword + '\n')




from keybert import KeyBERT
import os

dir_kw = 'corpus/Medical/kw/keybert/'
dir_all = 'corpus/Medical/txt/'
docs = os.listdir(dir_all)

kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')

os.makedirs(dir_kw + 'keybert_maxSum/')
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        keywords = kw_extractor.extract_keywords(texto, keyphrase_ngram_range=(1,15), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=10)
    with open(dir_kw + 'keybert_maxSum/' + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords[0][0].split():
            f_w.write('-' + keyword + '\n')


os.makedirs(dir_kw + 'keybert_maxMargRelevance/')
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        keywords = kw_extractor.extract_keywords(texto, keyphrase_ngram_range=(1,15), stop_words='english', use_mmr=True, diversity=0.7)
    with open(dir_kw + 'keybert_maxMargRelevance/' + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords[0][0].split():
            f_w.write('-' + keyword + '\n')
