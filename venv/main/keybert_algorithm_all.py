from keybert import KeyBERT


kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')

all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_keybert.txt'

with open(all) as f:
    texto = f.read()
    keywords = kw_extractor.extract_keywords(texto, keyphrase_ngram_range=(1,15), stop_words='english', top_n=200)

with open(all_kw, 'w') as f_w:
    for keyword in keywords[0][0].split():
        f_w.write('-' + keyword + '\n')
