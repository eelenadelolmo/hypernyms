import re
import os


# The first argument is the path to a document and the second argument is the patch to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora
def freq_calc(d, all):
    with open(all, 'r') as f:
        text_all = f.read()
        f.close()

    with open(d, 'r') as f:
        text = f.read()
        if re.search(r'Keywords: ?\n.+', text, re.DOTALL):
            keywords = re.search(r'Keywords: ?\n(.+)', text, re.DOTALL).group(1)
        else:
            keywords = text
        kw_list = keywords.split('\n')
        kw_freq_list = list()
        for kw in kw_list:
            kw_clean = re.sub('^- ?', '', kw)
            if len(kw_clean) > 0:
                kw_freq_list.append((kw_clean, text_all.count(kw_clean)))
        f.close()

    keywords_replace = str()
    for k, f_k in kw_freq_list:
        keywords_replace += '- ' + re.escape(k) + ' (' + re.escape(str(f_k)) + ')\n'

    text_replace = re.sub(keywords, keywords_replace, text)

    with open(d, 'w') as f:
        f.write(text_replace)
        f.close()


dir_all = 'corpus/Medical/txt_all.txt'
"""
dir_docs = 'corpus/Medical/kw/pke/topic_rank'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/text_rank'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/yake'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/keybert/keybert'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/keybert/keybert_maxMargRelevance'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/keybert/keybert_maxSum'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/rake/rake_degreeFreqRatio'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/rake/rake_degreeFreqRatio_length'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/rake/rake_metric_wordDegree_length'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/rake/rake_metric_wordFreq_length'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/tf_idf/tf_idf'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/tf_idf/tf_idf_sklearn'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc(dir_docs + '/' + doc, dir_all)
"""


dir_all_kw = 'corpus/Medical/txt_all_rake_degreeFreqRatio.txt'
freq_calc(dir_all_kw, dir_all)
"""
dir_all_kw = 'corpus/Medical/txt_all_rake_degreeFreqRatio_length.txt'
freq_calc(dir_all_kw, dir_all)
"""
"""
dir_all_kw = 'corpus/Medical/txt_all_rake_wordDegree_length.txt'
freq_calc(dir_all_kw, dir_all)
"""
"""
dir_all_kw = 'corpus/Medical/txt_all_rake_wordFreq_length.txt'
freq_calc(dir_all_kw, dir_all)
"""
"""
dir_all_kw = 'corpus/Medical/txt_all_text_rank.txt'
freq_calc(dir_all_kw, dir_all)
"""
"""
dir_all_kw = 'corpus/Medical/txt_all_yake.txt'
freq_calc(dir_all_kw, dir_all)
"""

