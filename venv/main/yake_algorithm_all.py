from yake import KeywordExtractor


kw_extractor = KeywordExtractor(lan="en", n=1, top=500)

all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_yake.txt'

with open(all) as f:
    texto = f.read()
    keywords = kw_extractor.extract_keywords(text=texto)
    keywords = [x for x, y in keywords]

with open(all_kw, 'w') as f_w:
    for keyword in keywords:
        f_w.write('- ' + keyword + '\n')
