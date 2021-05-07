# Ejecutar en terminal:
# !pip install -U spacy
# !pip install -U textacy
# python -m spacy download en_core_web_trf

import textacy
from textacy import extract
import en_core_web_trf

nlp = en_core_web_trf.load()

# changed in /home/elena/PycharmProjects/hypernyms/venv/lib/python3.8/site-packages/spacy/language.py
# nlp.max_length = 10000000000


# Get a list of noun phrases and deletes the overlapping shorter ones
def delete_overlapping(np_list):
    for i, elem_i in enumerate(np_list):
        for j in range(i):
            elem_j = np_list[j]
            if not elem_j:
                continue
            if elem_j.start <= elem_i.start and elem_j.end >= elem_i.end:
                # elem_i inside elem_j
                np_list[i] = None
                break
            elif elem_i.start <= elem_j.start and elem_i.end >= elem_j.end:
                # elem_j inside elem_i
                np_list[j] = None
            elif elem_i.end > elem_j.start and elem_i.start < elem_j.end:
                continue
                # raise ValueError('partial overlap?')
    return [elem for elem in np_list if elem]



# Approximately equivalent to '<DET>? <NUM>* (<ADJ> <CONJ>?)* (<NOUN>|<PROPN> (<PART> <CONJ>?)*)+'
pattern_np = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}]
pattern_pnp = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"*"}, {"POS": "PROPN", "OP":"+"}, {"POS": "NOUN", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}]
pattern_np_pp = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADP"}, {"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"POS": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}]



# For testing only
text = """
I am only testing the big big big well performing model. 
The president Obama was the very first EEUU president. 
There was a red, small fruit in the tree.
I want to match only the first noun phrase of every sentence of the text.
It was a time well spent.
"""

"""
for token in doc:
  print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
"""



all = 'corpus/Medical/txt_all.txt'

with open(all) as f:
    text = f.read().lower()

paras_list = text.split('\n\n\n')


# List of common noun phrases
salida_np = list()

# List of proper noun phrases
salida_pnp = list()

# List of noun phrases with prepositional complements
salida_np_pp = list()


for para in paras_list:
    doc = textacy.make_spacy_doc(para, lang=u'en_core_web_trf')
    salida_np.extend(list(textacy.extract.token_matches(doc, pattern_np)))
    salida_pnp.extend(list(textacy.extract.token_matches(doc, pattern_pnp)))
    salida_np_pp.extend(list(textacy.extract.token_matches(doc, pattern_np_pp)))


# Keeping only longest matches and adding proper and common noun phrases together
salida_np = delete_overlapping(salida_np)
salida_pnp = delete_overlapping(salida_pnp)
salida_np_pnp = salida_np + salida_pnp
salida_np_pp = delete_overlapping(salida_np_pp)

# Saving results to txt
with open('corpus/Medical/txt_all_noun_phrases_old.txt', 'w') as f_w:
    for e in salida_np_pnp:
        f_w.write('-' + e.text + '\n')

with open('corpus/Medical/txt_all_noun_phrases_pp_old.txt', 'w') as f_w:
    for e in salida_np_pp:
        f_w.write('-' + e.text + '\n')
