import os
import shutil



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
        texto = f.read()
        unique = unique.union(set(texto.split()))



## Getting word lists freqs of every text and their tf
# it is mandatory to have the whole metrics in order to calculate idf for once
text_words_freqs_tf = list()
for doc in docs:
    with open(dir_all + doc) as f:

        # word_list == list of the words
        texto = f.read()
        word_list = texto.split()

        # freq == dict with words:freq in the text
        freq = dict.fromkeys(unique, 0)
        for word in texto.split():
            freq[word] += 1

    e = dict()
    e['id'] = doc
    e['text'] = texto
    e['words'] = word_list
    e['freqs'] = freq
    e['tf'] = computeTF(freq, word_list)
    text_words_freqs_tf.append(e)

idf = computeIDF([x['freqs'] for x in text_words_freqs_tf])




dir_kw = 'corpus/Medical/kw/tfidf/'
shutil.rmtree(dir_kw, ignore_errors=True)
os.makedirs(dir_kw)

## Getting and saving the TF-IDF metrics for every text

for elem in text_words_freqs_tf:
    tfidf = computeTFIDF(elem['tf'], idf)
    with open(dir_kw + elem['id'], 'w') as f_w:
        f_w.write('Texto: \n' + elem['text'] + '\n\nKeywords: \n')

        words_text = elem['text'].split()

        for word in words_text:
            f_w.write('- ' + word + ': ' + str(tfidf[word]) + '\n')
