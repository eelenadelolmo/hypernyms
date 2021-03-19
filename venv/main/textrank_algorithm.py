from summa import keywords
import shutil
import os


""" Processing all corpora
# Interrupted by signal 9: SIGKILL
all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_textrank.txt'

with open(all) as f:
    texto = f.read()
    kws = keywords.keywords(texto)

with open(all_kw, 'w') as f_w:
    for keyword in kws.split():
        f_w.write('- ' + keyword + '\n')
"""


dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/textrank/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)
docs = os.listdir(dir_all)


for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read()
        kws = keywords.keywords(texto)
    with open(dir_kw + doc, 'w') as f_w:
        f_w.write('Texto: \n' + texto + '\n\nKeywords: \n')
        for keyword in kws.split():
            f_w.write('- ' + keyword + '\n')
