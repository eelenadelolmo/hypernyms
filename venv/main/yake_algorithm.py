from yake import KeywordExtractor
import shutil
import os



""" Processing all corpora

kw_extractor = KeywordExtractor(lan="en", n=1, top=500)

all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_yake.txt'

with open(all) as f:
    texto = f.read()
    keywords = kw_extractor.extract_keywords(text=texto)
    keywords = [x for x, y in keywords]

with open(all_kw, 'w') as f_w:
    for keyword in keywords:
        f_w.write('- ' + keyword + '\n')
"""


kw_extractor = KeywordExtractor(lan="en", n=1, top=5)

dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/yake/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)
docs = os.listdir(dir_all)

for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        keywords = kw_extractor.extract_keywords(text=texto)
        keywords = [x for x, y in keywords]
    with open(dir_kw + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in keywords:
            f_w.write('- ' + keyword + '\n')
