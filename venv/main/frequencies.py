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
                kw_clean = kw_clean.strip()
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('•', '', kw_root)
                kw_root = kw_root.strip()
                kw_words = kw_clean.split()
                kw_nonstop = [w for w in kw_words if not w in to_delete]
                kw_root_moreSpecific = 'no_kw_root_moreSpecific'

            if len(kw.split(' / ')) == 3:
                kw_kw = kw.split(' / ')[0]
                kw_root = kw.split(' / ')[1]
                kw_clean = re.sub('^- ?', '', kw_kw)
                kw_clean = re.sub('"', '', kw_clean)
                kw_clean = re.sub('•', '', kw_clean)
                kw_clean = kw_clean.strip()
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('"', '', kw_root)
                kw_root = re.sub('•', '', kw_root)
                kw_root = kw_root.strip()
                kw_words = kw_clean.split()
                kw_nonstop = [w for w in kw_words if not w in to_delete]
                kw_root_moreSpecific = kw.split(' / ')[2]
                kw_root_moreSpecific = re.sub('"', '', kw_root_moreSpecific)
                kw_root_moreSpecific = re.sub('"', '', kw_root_moreSpecific)
                kw_root_moreSpecific = re.sub('•', '', kw_root_moreSpecific)
                kw_root_moreSpecific = kw_root_moreSpecific.strip()

            # If there at lest one non-stopword word in the keyword and none word with less than 3 characters
            # if len(kw_nonstop) > 0 and len([w for w in kw_words if len(w) <= 2]) == 0:

            # If there is at least one non-stopword word in the keyword and none word is not an English word according to the NLTK dictionary
            # if len(kw_nonstop) > 0 and len([w for w in kw_words if w not in words.words()]) == 0:

            # All restrictions
            if len(kw_nonstop) > 0 and len([w for w in kw_nonstop if w not in words.words()]) == 0 and len([w for w in kw_words if len(w) <= 2]) == 0:

                if kw_root not in root_kw_dict and kw_root != "":
                    root_kw_dict[kw_root] = dict()

                if kw_root != "" and kw_root_moreSpecific not in root_kw_dict[kw_root] and kw_root_moreSpecific != "":
                    root_kw_dict[kw_root][kw_root_moreSpecific] = list()

                if kw_root != "" and kw_root_moreSpecific != "":
                    root_kw_dict[kw_root][kw_root_moreSpecific].append(kw_clean)

        f.close()


    # kw_dict_complex has the following structure:
    # { (root, root_freq): { (rootMoreSpec, rootMoreSpec_freq): [ (kw, kw_freq) ] } }
    kw_dict_complex = dict()

    # kw_dict has the following structure:
    # { (root, root_freq): [ (kw, kw_freq) ] }
    kw_dict = dict()

    freq_roots = dict()

    for e in root_kw_dict:
        if e not in freq_roots:
            freq_roots[e] = text_all.count(e.lower())

    freq_roots = {k: v for k, v in sorted(freq_roots.items(), key=lambda item: item[1], reverse=True)}

    text_replace = str()

    for r in freq_roots:

        freq_roots_moreSpec = dict()

        for kw_moreSpecific in root_kw_dict[r]:

            # if isinstance(kw_moreSpecific, str):
            if kw_moreSpecific not in freq_roots_moreSpec:
                freq_roots_moreSpec[kw_moreSpecific] = text_all.count(kw_moreSpecific.lower())

        freq_roots_moreSpec = {k: v for k, v in sorted(freq_roots_moreSpec.items(), key=lambda item: item[1], reverse=True)}

        # text_replace += '- ' + re.escape(r) + ' (' + re.escape(str(freq_roots[r])) + ')\n'

        for r_moreSpec in freq_roots_moreSpec:

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

            if r_moreSpec == 'no_kw_root_moreSpecific':
                kw_dict[ (r, freq_roots[r]) ] = list()
                for k in kw_freq:
                    # text_replace += '\t' + re.escape(k).replace('\\', '') + ' (' + re.escape(str(kw_freq[k])) + ')\n'
                    kw_dict[(r, freq_roots[r])].append((k, kw_freq[k]))
            else:
                if len(r_moreSpec.split()) > 1:

                    # Create the dict entry if it doesn't exist
                    if (r, freq_roots[r]) not in list(kw_dict_complex.keys()):
                        kw_dict_complex[(r, freq_roots[r])] = dict()

                    # text_replace += '\t+ ' + re.escape(r_moreSpec).replace('\\', '') + ' (' + re.escape(str(freq_roots_moreSpec[r_moreSpec])) + ')\n'
                    kw_dict_complex[(r, freq_roots[r])][(r_moreSpec, freq_roots_moreSpec[r_moreSpec])] = list()
                    for k in kw_freq:
                        # text_replace += '\t\t' + re.escape(k).replace('\\', '') + ' (' + re.escape(str(kw_freq[k])) + ')\n'
                        kw_dict_complex[(r, freq_roots[r])][(r_moreSpec, freq_roots_moreSpec[r_moreSpec])].append((k, kw_freq[k]))

    # Implementing another layer of classification, grouping more specific groups within less specific (which are substrings of the former)
    # Reminder:
    # kw_dict_complex has the following structure:
    # { (root, root_freq): { (rootMoreSpec, rootMoreSpec_freq): [ (kw, kw_freq) ] } }
    # And now it may have the following:
    # { (root, root_freq): { (rootMoreSpec, rootMoreSpec_freq): [ { (rootMoreSpec, rootMoreSpec_freq): [ (kw, kw_freq) ] } ] } }

    for (root, f) in kw_dict_complex:
        root_spec_list = list(kw_dict_complex[(root, f)].keys())
        for n, (e, f_e) in enumerate(root_spec_list):
            root_spec_list_others = root_spec_list[:]
            root_spec_list_others.pop(n)
            father = None
            sons = list()
            for (e_other, f_e_other) in root_spec_list_others:
                if e in e_other:
                    # Checking if the substring matching matches only full words
                    e_words = e.split()
                    e_other_words = e_other.split()
                    matches_full_words = True
                    for w in e_words:
                        if w not in e_other_words:
                            matches_full_words = False
                    if matches_full_words:
                        # Grouping (updating) with the less specific father only (the shortest)
                        if father is None or len(father[0]) > len(e):
                            father = (e, f_e)
                        sons.append((e_other, f_e_other))

            if len(sons) > 0 and father is not None:
                if father in kw_dict_complex[(root, f)]:
                    for son in sons:
                        if son in kw_dict_complex[(root, f)]:
                            new = {son: kw_dict_complex[(root, f)][son]}
                            kw_dict_complex[(root, f)][father].append(new)
                            kw_dict_complex[(root, f)].pop(son)

    # Reminder:
    # kw_dict has the following structure:
    # { (root, root_freq): [ (kw, kw_freq) ] }
    # kw_dict_complex has the following structure:
    # { (root, root_freq): { (rootMoreSpec, rootMoreSpec_freq): [ (kw, kw_freq) | { (rootMoreSpec, rootMoreSpec_freq): [ (kw, kw_freq) ] } ] } }

    # print(kw_dict)
    # print("_______")
    # print(kw_dict_complex)

    # Ordering with the most frequent before
    all_roots = list(set(list(kw_dict.keys()) + list(kw_dict_complex.keys())))
    all_roots = sorted(all_roots, key=lambda x: x[1], reverse=True)

    for root_general in all_roots:
        text_replace += '- ' + re.escape(root_general[0]) + ' (' + re.escape(str(root_general[1])) + ')\n'

        # Not all roots contain single-token keywords
        if root_general in list(kw_dict.keys()):
            for keywords_simple in kw_dict[root_general]:
                text_replace += '\t' + re.escape(keywords_simple[0]).replace('\\', '') + ' (' + re.escape(str(keywords_simple[1])) + ')\n'

        # Not all roots contain complex sub-roots
        if root_general in list(kw_dict_complex.keys()):
            for keyword_moreSpec in kw_dict_complex[root_general]:
                text_replace += '\t+ ' + re.escape(keyword_moreSpec[0]).replace('\\', '') + ' (' + re.escape(str(keyword_moreSpec[1])) + ')\n'

                for kw_final in kw_dict_complex[root_general][keyword_moreSpec]:

                    # If there is no more specific root
                    if isinstance(kw_final, tuple):
                        text_replace += '\t\t' + re.escape(kw_final[0]).replace('\\', '') + ' (' + re.escape(str(kw_final[1])) + ')\n'

                    if isinstance(kw_final, dict):
                        # There is always exactly one clave
                        for clave in kw_final:
                            text_replace += '\t\t+' + re.escape(clave[0]).replace('\\', '') + ' (' + re.escape(str(clave[1])) + ')\n'
                            for vals in kw_final[clave]:
                                text_replace += '\t\t\t' + re.escape(vals[0]).replace('\\', '') + ' (' + re.escape(str(vals[1])) + ')\n'

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
