from keybert import KeyBERT
import shutil
import os

kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')

dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/keybert/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)
docs = os.listdir(dir_all)

for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        keywords = kw_extractor.extract_keywords(texto, keyphrase_ngram_range=(1,15), stop_words='english', top_n=1)
    with open(dir_kw + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords[0][0].split():
            f_w.write('-' + keyword + '\n')
