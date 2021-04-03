from summa import keywords


all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_text_rank.txt'

with open(all) as f:
    texto = f.read()
    kws = keywords.keywords(texto)

with open(all_kw, 'w') as f_w:
    for keyword in kws.split():
        f_w.write('- ' + keyword + '\n')
