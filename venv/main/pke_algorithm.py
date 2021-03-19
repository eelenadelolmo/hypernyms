import pke
import shutil
import os

""" Processing all corpora
# Text of length 7620447 exceeds maximum of 1000000. The parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input. This means long texts may cause memory allocation errors. If you're not using the parser or NER, it's probably safe to increase the `nlp.max_length` limit. The limit is in number of characters, so you can check whether your inputs are too long by checking `len(text)`.
all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_pke_topicrank.txt'

with open(all) as f:
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=all, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keywords = extractor.get_n_best(n=10)

with open(all_kw, 'w') as f_w:
    for keyword in keywords:
        f_w.write('- ' + keyword + '\n')
"""


dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/pke/topicrank/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)
docs = os.listdir(dir_all)

for doc in docs:
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=dir_all + doc, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keywords = extractor.get_n_best(n=10)
    with open(dir_kw + doc, 'w') as f_w:
        with open(dir_all + doc) as f:
            f_w.write('Texto: \n' + f.read() + '\n\nKeywords: \n')
            for keyword in keywords:
                f_w.write('- ' + keyword[0] + '\n')
