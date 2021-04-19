# Ejecutar en terminal:
# !pip install -U spacy
# !pip install -U textacy
# python -m spacy download en_core_web_trf

import textacy
from textacy import extract
import en_core_web_trf

nlp = en_core_web_trf.load()

doc = textacy.make_spacy_doc("I am only testing the model by now", lang=u'en_core_web_trf')
print(list(textacy.extract.regex_matches(doc, "POS:DET:? POS:ADJ:? POS:NOUN:+")))