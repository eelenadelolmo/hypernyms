from rake_nltk import Rake

dir_all = 'corpus/Medical/txt_all.txt'

r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

with open(dir_all) as f:
    texto = f.read()
    r.extract_keywords_from_text(texto)
    r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.