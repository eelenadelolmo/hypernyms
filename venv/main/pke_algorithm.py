import pke
import shutil
import os


dir_all = 'corpus/Medical/txt/'
dir_kw = 'corpus/Medical/kw/pke/topic_rank/'
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
