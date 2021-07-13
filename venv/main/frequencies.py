import re
import os
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words


# The first argument is the path to a document and the second argument is the path to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora
def freq_calc(d, all):
    with open(all, 'r') as f:
        text_all = f.read().lower()
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
                kw_freq_list.append((kw_clean, text_all.count(kw_clean.lower())))
        f.close()

    keywords_replace = str()
    for k, f_k in kw_freq_list:
        keywords_replace += '- ' + re.escape(k) + ' (' + re.escape(str(f_k)) + ')\n'

    text_replace = re.sub(re.escape(keywords), re.escape(keywords_replace), text).replace('\\', '')

    with open(d, 'w') as f:
        f.write(text_replace)
        f.close()


# The first argument is the path to a document and the second argument is the patch to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora and reorders the keyword by frequency
def freq_calc_order_by_freq(d, all):
    with open(all, 'r') as f:
        text_all = f.read().lower()
        f.close()

    with open(d, 'r') as f:
        text = f.read()
        if re.search(r'Keywords: ?\n.+', text, re.DOTALL):
            keywords = re.search(r'Keywords: ?\n(.+)', text, re.DOTALL).group(1)
        else:
            keywords = text
        kw_list = keywords.split('\n')
        kw_freq = dict()
        for kw in kw_list:
            kw_clean = re.sub('^- ?', '', kw)
            if len(kw_clean) > 0:
                kw_freq[kw_clean] = text_all.count(kw_clean.lower())
        f.close()

    kw_freq = {k: v for k, v in sorted(kw_freq.items(), key=lambda item: item[1], reverse=True)}

    keywords_replace = str()
    for k in kw_freq:
        keywords_replace += '- ' + re.escape(k) + ' (' + re.escape(str(kw_freq[k])) + ')\n'

    text_replace = re.sub(re.escape(keywords), re.escape(keywords_replace), text).replace('\\', '')

    with open(d, 'w') as f:
        f.write(text_replace)
        f.close()


# The first argument is the path to a document and the second argument is the path to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora and reorders the keyword by frequency
def freq_calc_order_by_freq_stopwords(d, all):
    to_delete = stopwords.words('english')
    with open(all, 'r') as f:
        text_all = f.read().lower()
        f.close()

    with open(d, 'r') as f:
        text = f.read()
        if re.search(r'Keywords: ?\n.+', text, re.DOTALL):
            keywords = re.search(r'Keywords: ?\n(.+)', text, re.DOTALL).group(1)
        else:
            keywords = text
        kw_list = keywords.split('\n')
        kw_freq = dict()
        for kw in kw_list:
            kw_clean = re.sub('^- ?', '', kw)
            kw_clean = re.sub('"', '', kw_clean)
            kw_words = kw_clean.split()
            kw_nonstop = [w for w in kw_words if not w in to_delete]

            # If there at lest one non-stopword word in the keyword and none word with less than 3 characters
            # if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if len(w) <= 2]) == 0:

            # If there is at least one non-stopword word in the keyword and none word is not an English word according to the NLTK dictionary
            # if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if w not in words.words()]) == 0:

            # All restrictions
            if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if w not in words.words()]) == 0 and len([w for w in kw_nonstop if len(w) <= 2]) == 0:
                kw_freq[kw_clean] = 0
                for k in kw_nonstop:
                    kw_freq[kw_clean] += text_all.count(k.lower())
                kw_freq[kw_clean] = int(kw_freq[kw_clean] / len(kw_nonstop))

        f.close()

    kw_freq = {k: v for k, v in sorted(kw_freq.items(), key=lambda item: item[1], reverse=True)}

    keywords_replace = str()
    for k in kw_freq:
        keywords_replace += '- ' + re.escape(k) + ' (' + re.escape(str(kw_freq[k])) + ')\n'

    text_replace = re.sub(re.escape(keywords), re.escape(keywords_replace), text).replace('\\', '')

    with open(d, 'w') as f:
        f.write(text_replace)
        f.close()



# The first argument is the path to a document and the second argument is the path to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora and reorders the keyword by frequency
def freq_calc_order_by_freq_stopwords_roots(d, all):
    to_delete = stopwords.words('english')
    root_kw_dict = dict()

    with open(all, 'r') as f:
        text_all = f.read().lower()
        f.close()

    with open(d, 'r') as f:
        text = f.read()
        if re.search(r'Keywords: ?\n.+', text, re.DOTALL):
            keywords = re.search(r'Keywords: ?\n(.+)', text, re.DOTALL).group(1)
        else:
            keywords = text
        kw_line = keywords.split('\n')
        for kw in kw_line:
            if len(kw.split(' / ')) > 1:
                kw_kw = kw.split(' / ')[0]
                kw_root = kw.split(' / ')[1]
                kw_clean = re.sub('^- ?', '', kw_kw)
                kw_clean = re.sub('"', '', kw_clean)
                kw_clean = re.sub('•', '', kw_clean)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('•', '', kw_root)
                kw_words = kw_clean.split()
                kw_nonstop = [w for w in kw_words if not w in to_delete]

                # If there at lest one non-stopword word in the keyword and none word with less than 3 characters
                # if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if len(w) <= 2]) == 0:

                # If there is at least one non-stopword word in the keyword and none word is not an English word according to the NLTK dictionary
                # if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if w not in words.words()]) == 0:

                # All restrictions
                if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if w not in words.words()]) == 0 and len([w for w in kw_nonstop if len(w) <= 2]) == 0:

                    if kw_root not in root_kw_dict:
                        root_kw_dict[kw_root] = list()

                    root_kw_dict[kw_root].append(kw_clean)

    f.close()

    freq_roots = dict()

    for e in root_kw_dict:
        if e not in freq_roots:
            freq_roots[e] = text_all.count(e.lower())

    freq_roots = {k: v for k, v in sorted(freq_roots.items(), key=lambda item: item[1], reverse=True)}

    text_replace = str()

    for r in freq_roots:
        kw_freq = dict()
        kw_list = root_kw_dict[r]

        for k in kw_list:
            kw_words = k.split()
            kw_nonstop = [w for w in kw_words if not w in to_delete]

            kw_freq[k] = 0
            for k_n in kw_nonstop:
                kw_freq[k] += text_all.count(k_n.lower())
            kw_freq[k] = int(kw_freq[k] / len(kw_nonstop))

        kw_freq = {k: v for k, v in sorted(kw_freq.items(), key=lambda item: item[1], reverse=True)}

        text_replace += '- ' + re.escape(r) + ' (' + re.escape(str(freq_roots[r])) + ')\n'
        for k in kw_freq:
            text_replace += '\t' + re.escape(k).replace('\\', '') + ' (' + re.escape(str(kw_freq[k])) + ')\n'

    with open(d, 'w') as f:
        f.write(text_replace)
        f.close()


# The first argument is the path to a document and the second argument is the path to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora and reorders the keyword by frequency
def freq_calc_order_by_freq_stopwords_roots_moreSpecific(d, all):
    to_delete = stopwords.words('english')
    root_kw_dict = dict()

    with open(all, 'r') as f:
        text_all = f.read().lower()
        f.close()

    with open(d, 'r') as f:
        text = f.read()
        if re.search(r'Keywords: ?\n.+', text, re.DOTALL):
            keywords = re.search(r'Keywords: ?\n(.+)', text, re.DOTALL).group(1)
        else:
            keywords = text
        kw_line = keywords.split('\n')
        for kw in kw_line:
            if len(kw.split(' / ')) == 2:
                kw_kw = kw.split(' / ')[0]
                kw_root = kw.split(' / ')[1]
                kw_clean = re.sub('^- ?', '', kw_kw)
                kw_clean = re.sub('"', '', kw_clean)
                kw_clean = re.sub('•', '', kw_clean)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('•', '', kw_root)
                kw_words = kw_clean.split()
                kw_nonstop = [w for w in kw_words if not w in to_delete]
                kw_root_moreSpecific = 'no_kw_root_moreSpecific'

            if len(kw.split(' / ')) == 3:
                kw_kw = kw.split(' / ')[0]
                kw_root = kw.split(' / ')[1]
                kw_clean = re.sub('^- ?', '', kw_kw)
                kw_clean = re.sub('"', '', kw_clean)
                kw_clean = re.sub('•', '', kw_clean)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('•', '', kw_root)
                kw_words = kw_clean.split()
                kw_nonstop = [w for w in kw_words if not w in to_delete]
                kw_root_moreSpecific = kw.split(' / ')[2]
                kw_root_moreSpecific = re.sub('"', '', kw_root_moreSpecific)
                kw_root_moreSpecific = re.sub('"', '', kw_root_moreSpecific)
                kw_root_moreSpecific = re.sub('•', '', kw_root_moreSpecific)

            # If there at lest one non-stopword word in the keyword and none word with less than 3 characters
            # if len(kw_nonstop) > 0 and len([w for w in kw_words if len(w) <= 2]) == 0:

            # If there is at least one non-stopword word in the keyword and none word is not an English word according to the NLTK dictionary
            # if len(kw_nonstop) > 0 and len([w for w in kw_words if w not in words.words()]) == 0:

            # All restrictions
            if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if w not in words.words()]) == 0 and len([w for w in kw_words if len(w) <= 2]) == 0:

                if kw_root not in root_kw_dict:
                    root_kw_dict[kw_root] = dict()

                if kw_root_moreSpecific not in root_kw_dict[kw_root]:
                    root_kw_dict[kw_root][kw_root_moreSpecific] = list()

                root_kw_dict[kw_root][kw_root_moreSpecific].append(kw_clean)
                
        f.close()

    freq_roots = dict()

    for e in root_kw_dict:
        if e not in freq_roots:
            freq_roots[e] = text_all.count(e.lower())

    freq_roots = {k: v for k, v in sorted(freq_roots.items(), key=lambda item: item[1], reverse=True)}

    text_replace = str()

    for r in freq_roots:

        freq_roots_moreSpec = dict()
        for kw_moreSpecific in root_kw_dict[r]:
            if kw_moreSpecific not in freq_roots_moreSpec:
                freq_roots_moreSpec[kw_moreSpecific] = text_all.count(kw_moreSpecific.lower())

        freq_roots_moreSpec = {k: v for k, v in sorted(freq_roots_moreSpec.items(), key=lambda item: item[1], reverse=True)}

        for r_moreSpec in root_kw_dict[r]:

            kw_freq = dict()
            kw_moreSpecific_list = root_kw_dict[r][r_moreSpec]
            for k in kw_moreSpecific_list:
                kw_words = k.split()
                kw_nonstop = [w for w in kw_words if not w in to_delete]

                kw_freq[k] = 0
                for k_n in kw_nonstop:
                    kw_freq[k] += text_all.count(k_n.lower())
                kw_freq[k] = int(kw_freq[k] / len(kw_nonstop))

            kw_freq = {k: v for k, v in sorted(kw_freq.items(), key=lambda item: item[1], reverse=True)}

            text_replace += '- ' + re.escape(r) + ' (' + re.escape(str(freq_roots[r])) + ')\n'

            if r_moreSpec == 'no_kw_root_moreSpecific':
                for k in kw_freq:
                    text_replace += '\t' + re.escape(k).replace('\\', '') + ' (' + re.escape(str(kw_freq[k])) + ')\n'
            else:
                text_replace += '\t+ ' + re.escape(r_moreSpec).replace('\\', '') + ' (' + re.escape(str(freq_roots_moreSpec[r_moreSpec])) + ')\n\t\t'
                for k in kw_freq:
                    text_replace += '\t' + re.escape(k).replace('\\', '') + ' (' + re.escape(str(kw_freq[k])) + ')\n'

    with open(d, 'w') as f:
        f.write(text_replace)
        f.close()



# The first argument is the path to a document and the second argument is the patch to a document with the whole corpora
# Rewrites the document with the absolute frequency of every keyword in the whole corpora
def freq_calc_withScore(d, all):
    with open(all, 'r') as f:
        text_all = f.read().lower()
        f.close()

    with open(d, 'r') as f:
        text = f.read()
        if re.search(r'Keywords by value: ?\n.+', text, re.DOTALL):
            keywords = re.search(r'Keywords by value: ?\n(.+)', text, re.DOTALL).group(1)
        else:
            keywords = text
        kw_list = keywords.split('\n')
        kw_freq_list = list()
        for kw in kw_list:
            kw_clean = re.sub('^- ?', '', kw)
            if len(kw_clean) > 0:
                fin_str = kw_clean.rfind(': ')
                kw_freq_list.append((kw_clean, text_all.count(kw_clean[:fin_str].lower())))
        f.close()

    keywords_replace = str()
    for k, f_k in kw_freq_list:
        keywords_replace += '- ' + re.escape(k) + ' (' + re.escape(str(f_k)) + ')\n'

    text_replace = re.sub(re.escape(keywords), re.escape(keywords_replace), text).replace('\\', '')

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
    freq_calc_withScore(dir_docs + '/' + doc, dir_all)
"""
"""
dir_docs = 'corpus/Medical/kw/tf_idf/tf_idf_sklearn'
docs = os.listdir(dir_docs)
for doc in docs:
    freq_calc_withScore(dir_docs + '/' + doc, dir_all)
"""
"""
dir_all_kw = 'corpus/Medical/txt_all_rake_degreeFreqRatio.txt'
freq_calc(dir_all_kw, dir_all)
"""
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



"""
dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_old.txt'
freq_calc_order_by_freq(dir_all_kw, dir_all)

dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_pp_old.txt'
freq_calc_order_by_freq(dir_all_kw, dir_all)
"""


"""
# dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_isWord_longerThanTwo.txt'
dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_isWord.txt'
# dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_isWord.txt'
freq_calc_order_by_freq_stopwords(dir_all_kw, dir_all)

"""
"""
dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_plus_barePP_isWord_longerThanTwo.txt'
freq_calc_order_by_freq_stopwords(dir_all_kw, dir_all)
"""
"""
dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_adjectives_isWord_longerThanTwo.txt'
freq_calc_order_by_freq_stopwords(dir_all_kw, dir_all)
"""

"""
dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_adjectives_coord_isWord_longerThanTwo.txt'
freq_calc_order_by_freq_stopwords_roots(dir_all_kw, dir_all)
"""
dir_all_kw = 'corpus/Medical/txt_all_noun_phrases_adjectives_moreSpecific_coord_isWord_longerThanTwo.txt'
freq_calc_order_by_freq_stopwords_roots_moreSpecific(dir_all_kw, dir_all)