# Ejecutar en terminal:
# !pip install -U spacy
# !pip install -U textacy
# python -m spacy download en_core_web_trf

import textacy
from textacy import extract
import en_core_web_trf

nlp = en_core_web_trf.load()

doc = textacy.make_spacy_doc("I am only testing the big big big well performing model very well dressed by now. The president Obama was the very first EEUU president. There was a red, small fruit in the tree.", lang=u'en_core_web_trf')

# print(list(doc.sents))

for token in doc:
  print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

# Equivalent to '<DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<NOUN>|<PROPN> <PART>?)+'
pattern_np = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"POS": "PART", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "PART", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "PART", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}]
pattern_pnp = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"*"}, {"POS": "PROPN", "OP":"+"}, {"POS": "NOUN", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "PART", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "PART", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "PART", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}]

salida_np = list(textacy.extract.token_matches(doc, pattern_np))
salida_pnp = list(textacy.extract.token_matches(doc, pattern_pnp))

salida = salida_np + salida_pnp

# take the longest when overlapping
for i, el_i in enumerate(salida):
    for j in range(i):
        el_j = salida[j]
        if not el_j:
            continue
        if el_j.start <= el_i.start and el_j.end >= el_i.end:
            # el_i inside el_j
            salida[i] = None
            break
        elif el_i.start <= el_j.start and el_i.end >= el_j.end:
            # el_j inside el_i
            salida[j] = None
        elif el_i.end > el_j.start and el_i.start < el_j.end:
            continue
            # raise ValueError('partial overlap?')
salida = [el for el in salida if el]

for e in salida:
    print("Noun phrase:", e)
