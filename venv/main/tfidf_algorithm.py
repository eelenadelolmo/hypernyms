import os
import shutil
import nltk

dir_parent = 'corpus/Medical/kw/tf_idf/'
shutil.rmtree(dir_parent, ignore_errors=True)
os.makedirs(dir_parent)


#_____________________________________________________________________________________________________________________

## Creating sentence and word tokeniser

from nltk.tokenize.punkt import PunktSentenceTokenizer
stoker = PunktSentenceTokenizer()
s_tokers = {'en': stoker}
sent_tokenizer = s_tokers.get('en', stoker)

tokenisers = {'en': nltk.word_tokenize}
tokeniser = tokenisers.get('en', nltk.word_tokenize)



#_____________________________________________________________________________________________________________________

#### Testing the original TF-IDF algorithm ####


# The argument is a frequency dictionary word:freq_abs and the list of words
# returns a dictionary word:tf, tf consisting of the freq of the word in the text
def computeTF(f_dict, w_list):
  tfDict = dict()
  n_words = len(w_list)
  for word, count in f_dict.items():
    tfDict[word] = count / n_words
  return tfDict


# The argument is a list of frequency dictionaries word:freq_abs of every text in the corpora
# returns a dictionary word:idf, idf consisting of the log of the inverse of the frequency of the word in the texts
def computeIDF(documents):
    import math
    n_docs = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(n_docs / float(val))

    return idfDict


# The arguments are the output of the previous functions (dictionary of tfs and dictionary of idfs)
# returns a dictionary word:tf_idf, tf_idf consisting of the TI-IDF value for a given term
def computeTFIDF(tf, idfs):
  tfidf = dict()
  for word, val in tf.items():
    tfidf[word] = val * idfs[word]
  return tfidf


dir_all = 'corpus/Medical/txt/'
docs = os.listdir(dir_all)

## Getting a set of unique words
unique = set()
for doc in docs:
    with open(dir_all + doc) as f:
        texto = f.read().lower()

        sents = sent_tokenizer.tokenize(texto)
        toks = list()
        for sent in sents:
            toks.extend(tokeniser(sent))

        unique = unique.union(set(toks))


## Getting word lists freqs of every text and their tf
# it is mandatory to have the whole metrics in order to calculate idf for once
text_words_freqs_tf = list()
for doc in docs:
    with open(dir_all + doc) as f:

        # word_list == list of the words
        texto = f.read().lower()

        sents = sent_tokenizer.tokenize(texto)
        word_list = list()
        for sent in sents:
            word_list.extend(tokeniser(sent))

        # freq == dict with words:freq in the text
        freq = dict.fromkeys(unique, 0)
        for word in word_list:
            freq[word] += 1

    e = dict()
    e['id'] = doc
    e['text'] = texto
    e['words'] = word_list
    e['freqs'] = freq
    e['tf'] = computeTF(freq, word_list)
    text_words_freqs_tf.append(e)

idf = computeIDF([x['freqs'] for x in text_words_freqs_tf])


dir_kw = 'corpus/Medical/kw/tf_idf/tf_idf/'
shutil.rmtree(dir_parent, ignore_errors=True)
os.makedirs(dir_kw)


## Getting and saving the TF-IDF metrics for every text

for elem in text_words_freqs_tf:
    tfidf = computeTFIDF(elem['tf'], idf)
    with open(dir_kw + elem['id'], 'w') as f_w:
        f_w.write('Texto: \n' + elem['text'] + '\n\nKeywords by value: \n')

        sents = sent_tokenizer.tokenize(elem['text'])
        words_text = list()
        for sent in sents:
            words_text.extend(tokeniser(sent))

        word_tfif = dict()
        for word in words_text:
            word_tfif[word] = tfidf[word]

        word_tfif = {k: v for k, v in sorted(word_tfif.items(), key=lambda item: item[1], reverse=True)}

        for word in word_tfif:
            f_w.write('- ' + word + ': ' + str(word_tfif[word]) + '\n')


# _____________________________________________________________________________________________________________________

#### Testing the sklearn algorithm ####

dir_kw_sklearn = 'corpus/Medical/kw/tf_idf/tf_idf_sklearn/'
shutil.rmtree(dir_kw_sklearn, ignore_errors=True)
os.makedirs(dir_kw_sklearn)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([x['text'] for x in text_words_freqs_tf])
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)

for n, elem in enumerate(text_words_freqs_tf):
    with open(dir_kw_sklearn + elem['id'], 'w') as f_w:
        f_w.write('Texto: \n' + elem['text'] + '\n\nKeywords by value: \n')

        sents = sent_tokenizer.tokenize(elem['text'])
        words_text = list()
        for sent in sents:
            words_text.extend(tokeniser(sent))

        df_texto = df.iloc[[n]]

        word_tfif_sklearn = dict()
        for word in words_text:
            if word.lower() in df_texto.columns:
                word_tfif_sklearn[word] = str(df_texto[word.lower()][n])
            else:
                print("Not matched because of different tokenisation:", word)

        word_tfif_sklearn = {k: v for k, v in sorted(word_tfif_sklearn.items(), key=lambda item: item[1], reverse=True)}

        for word in word_tfif_sklearn:
            f_w.write('- ' + word + ': ' + str(word_tfif_sklearn[word]) + '\n')
