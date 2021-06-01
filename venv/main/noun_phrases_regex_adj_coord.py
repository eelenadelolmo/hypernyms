# pip install spacy==2.3.1
# python -m spacy download en_core_web_lg
# pip install textacy==0.10.0

import textacy
import en_core_web_lg

nlp = en_core_web_lg.load()


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


# Pattern based on fine-grained tag (must be searched with pos_regex_matches_tag)
pattern_np = '<CD>? ((<RB>|<RBR>|<RBS>)? (<RB>|<RBR>|<RBS>)? (<JJ>|<JJR>|<JJS>|<VBG>|<VBN>)+ <CC>?)* (<NNP>|<NN>|<NNS>)+ ((<RB>|<RBR>|<RBS>)? (<RB>|<RBR>|<RBS>)? <VBN> <CC>?)*'

# Pattern based on coarse tag because the tag <,> appears to be not matched (must be searched with pos_regex_matches)
pattern_np_punct = '<NUM>? (<ADV>? <ADV>? (<ADJ>|<VERB>)+ (<PUNCT> (<ADJ>|<VERB>))? <CCONJ>?)* (<NOUN>|<PROPN>)+ (<ADV>? <ADV>? <VERB> (<PUNCT> <VERB>)? <CCONJ>?)*'

# Pattern based on fine-grained tag (must be searched with pos_regex_matches_tag)
pattern_np_pp = '<CD>? ((<RB>|<RBR>|<RBS>)? (<RB>|<RBR>|<RBS>)? (<JJ>|<JJR>|<JJS>|<VBG>|<VBN>)+ <CC>?)* (<NNP>|<NN>|<NNS>)+ ((<RB>|<RBR>|<RBS>)? (<RB>|<RBR>|<RBS>)? <VBN> <CC>?)* <IN> (<NNP>|<NN>|<NNS>)+'

# Pattern based on coarse tag because the tag <,> appears to be not matched (must be searched with pos_regex_matches)
pattern_np_punct_pp = '<NUM>? (<ADV>? <ADV>? (<ADJ>|<VERB>)+ (<PUNCT> (<ADJ>|<VERB>))? <CCONJ>?)* (<NOUN>|<PROPN>)+ (<ADV>? <ADV>? <VERB> (<PUNCT> <VERB>)? <CCONJ>?)* <ADP> (<NOUN>|<PROPN>)+'

# Pattern based on fine-grained tag (must be searched with pos_regex_matches_tag)
pattern_np_jj = '((<JJ>|<JJR>|<JJS>|<VBG>|<VBN>)+ <CC>?)* (<NN>|<NNP>|<NNS>)+ (<VBN> <CC>?)*'

# Pattern based on coarse tag because the tag <,> appears to be not matched (must be searched with pos_regex_matches)
pattern_np_jj_punct = '((<ADJ>|>VERB>)+ (<PUNCT> <ADJ>|<VERB>)? <CCONJ>?)* (<NOUN>|<PROPN>)+ (<VERB> (<PUNCT> <VERB>)? <CCONJ>?)*'

# For testing only
text = """
I am only testing the big big big well performing models. 
The president Obama was the very first EEUU president. 
There was a red, small and juicy fruit in the tree.
I want to match only the first noun phrase of every sentence of the text.
It was a time well spent.
It was a time spent.
It seems to be not dangerous, however other immunomodulating therapies may comprise different problems.
The most interesting first time appearance and.
My classroom friend John.
The EEUU president.
The strongest man.
A stronger woman.
A strong woman.
Men and women came to visit my mother and father.
They came to visit my aunt and my uncle.
They found rests of skin tissue.
They found rests of black tissue.
"""

"""
doc = textacy.make_spacy_doc(text, lang=u'en_core_web_lg')


## Matching only adjectives and adverbs
matches = list(textacy.extract.pos_regex_matches_tag(doc, pattern_np))

matches_punct = list(textacy.extract.pos_regex_matches(doc, pattern_np_punct))

matches_punct_ok = list()
for i, e in enumerate(matches_punct):
    if ',' in e.lower_:
        matches_punct_ok.append(e)

matches_all = delete_overlapping(matches + matches_punct_ok)

matches_clean = list()
for e in matches_all:
    for t in e:
        if ((t.pos_ == 'ADV' or t.pos_ == 'CCONJ') and t.head.tag_ not in  ['JJ','JJR','JJS','VBN','VBG']):
            to_delete = t.text
            to_add = e.text.replace(to_delete, "").replace('however', "").strip()
        else:
            to_add = e.text.replace('however', "").strip()

    matches_clean.append(to_add)

print("Solo adjetivos y adverbios:", matches_clean)

## Matching NPs plus bare PP complements
matches_pp = list(textacy.extract.pos_regex_matches_tag(doc, pattern_np_pp))

matches_punct_pp = list(textacy.extract.pos_regex_matches(doc, pattern_np_punct_pp))

matches_punct_pp_ok = list()
for i, e in enumerate(matches_punct_pp):
    if ',' in e.lower_:
        matches_punct_pp_ok.append(e)

matches_all_pp = delete_overlapping(matches_pp + matches_punct_pp_ok)

matches_clean_pp = list()
for e in matches_all_pp:
    for t in e:
        if ((t.pos_ == 'ADV' or t.pos_ == 'CCONJ') and t.head.tag_ not in  ['JJ','JJR','JJS','VBN','VBG']):
            to_delete = t.text
            to_add = e.text.replace(to_delete, "").replace('however', "").strip()
        else:
            to_add = e.text.replace('however', "").strip()

    matches_clean_pp.append(to_add)

print("Con complementos preposicionales escuetos:", matches_clean_pp)



## Matching only adjectives
matches_jj = list(textacy.extract.pos_regex_matches_tag(doc, pattern_np_jj))

matches_jj_punct = list(textacy.extract.pos_regex_matches(doc, pattern_np_jj_punct))

matches_jj_punct_ok = list()
for i, e in enumerate(matches_jj_punct):
    if ',' in e.lower_:
        matches_jj_punct_ok.append(e)

matches_all_jj = delete_overlapping(matches_jj + matches_jj_punct_ok)

matches_clean_jj = list()
for e in matches_all_jj:
    for t in e:
        if ((t.pos_ == 'ADV' or t.pos_ == 'CCONJ') and t.head.tag_ not in  ['JJ','JJR','JJS','VBN','VBG']):
            to_delete = t.text
            to_add = e.text.replace(to_delete, "").replace('however', "").strip()
        else:
            to_add = e.text.replace('however', "")

    matches_clean_jj.append(to_add)

print("Solo adjetivos:", matches_all_jj)


for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop, token.head.text)
"""

all = 'corpus/Medical/txt_all.txt'

with open(all) as f:
    text = f.read().lower()

paras_list = text.split('\n\n\n')

# List of noun phrases
salida_np = list()

# List of noun phrases plus bare preposition phrases
salida_np_pp = list()

# List of nouns plus adjective complements
salida_np_jj = list()

for para in paras_list:
    doc = textacy.make_spacy_doc(para, lang=u'en_core_web_lg')

    """
    matches = list(textacy.extract.pos_regex_matches_tag(doc, pattern_np))
    salida_np.extend(matches)

    matches_pp = list(textacy.extract.pos_regex_matches_tag(doc, pattern_np_pp))
    salida_np_pp.extend(matches_pp)
    """

    matches_jj = list(textacy.extract.pos_regex_matches_tag(doc, pattern_np_jj))
    salida_np_jj.extend(matches_jj)
    """
    matches_punct = list(textacy.extract.pos_regex_matches(doc, pattern_np_punct))
    matches_punct_ok = list()
    for i, e in enumerate(matches_punct):
        if ',' in e.lower_:
            matches_punct_ok.append(e)
    salida_np.extend(matches_punct_ok)

    matches_punct_pp = list(textacy.extract.pos_regex_matches(doc, pattern_np_punct_pp))
    matches_punct_pp_ok = list()
    for i, e in enumerate(matches_punct_pp):
        if ',' in e.lower_:
            matches_punct_pp_ok.append(e)
    salida_np_pp.extend(matches_punct_pp_ok)
    """
    matches_punct_jj = list(textacy.extract.pos_regex_matches(doc, pattern_np_jj_punct))
    matches_punct_jj_ok = list()
    for i, e in enumerate(matches_punct_jj):
        if ',' in e.lower_:
            matches_punct_jj_ok.append(e)
    salida_np_jj.extend(matches_punct_jj_ok)
"""
salida_np = delete_overlapping(salida_np)
matches_clean = list()
for e in salida_np:
    for t in e:
        if ((t.pos_ == 'ADV' or t.pos_ == 'CCONJ') and t.head.tag_ not in  ['JJ','JJR','JJS','VBN','VBG']):
            to_delete = t.text
            to_add = e.text.replace(to_delete, "").replace('however', "").strip()
        else:
            to_add = e.text.replace('however', "")
    matches_clean.append(to_add)

salida_np_pp = delete_overlapping(salida_np_pp)
matches_clean_pp = list()
for e in salida_np_pp:
    for t in e:
        if ((t.pos_ == 'ADV' or t.pos_ == 'CCONJ') and t.head.tag_ not in  ['JJ','JJR','JJS','VBN','VBG']):
            to_delete = t.text
            to_add = e.text.replace(to_delete, "").replace('however', "").strip()
        else:
            to_add = e.text.replace('however', "")
    matches_clean_pp.append(to_add)
salida_np_jj = delete_overlapping(salida_np_jj)
"""
matches_clean_jj = list()
for e in salida_np_jj:

    to_add = list()
    has_coord = False

    list_nn = list()
    root = None

    for t in e:

        print(t.text, t.lemma_, t.pos_, t.tag_, t.dep_, t.shape_, t.is_alpha, t.is_stop, t.head.text)
        if t.pos_ == 'NOUN':
            list_nn.append(t)
        if len(list_nn) > 0:
            root = list_nn[-1]
            root_complete = [x for x in list(root.subtree) if x.text in e.text.split()]

        if t.pos_ == 'CCONJ' or t.pos_ == 'PUNCT':
            has_coord = True

    if has_coord:
        print('_________________________________________________________________________________')
        print('Contiene coordinación:', e.text)

        if root:

            if ',' not in e.text.replace(',', ' ,').split():
                conj = [x for x in e if x.dep_ == 'cc']
                if len(conj) > 0:
                    conj = conj[0]
                    first_head = conj.head
                    second_head = [x for x in e if x.dep_ == 'conj']

                    if len(second_head) > 0:
                        second_head = second_head[0]
                        second_complete = [x for x in list(second_head.subtree) if x.text in e.text.split()]
                        first_complete = [x for x in list(first_head.subtree) if
                                          x not in second_complete and x.pos_ != 'CCONJ' and x.text in e.text.split()]
                        root_complete_no_coords = [x for x in list(root.subtree) if
                                                   x.text in e.text.split() and x not in first_complete + second_complete and x.pos_ != 'CCONJ']

                        if len(root_complete_no_coords) > 0 and len([x.text for x in root_complete_no_coords]) == len(
                                set([x.text for x in root_complete_no_coords])):
                            print('El núcleo sin coordinantes es:', " ".join([i.text for i in root_complete_no_coords]))
                            print('El SN analizado es:', e.text)
                            print('El primer coordinante es:', " ".join([i.text for i in first_complete]))
                            print('El segundo coordinante es:', " ".join([i.text for i in second_complete]))
                            too_add_1 = " ".join([i.text for i in first_complete]) + " " + " ".join(
                                [i.text for i in root_complete_no_coords])
                            too_add_2 = " ".join([i.text for i in second_complete]) + " " + " ".join(
                                [i.text for i in root_complete_no_coords])
                            to_add.append((too_add_1, root))
                            to_add.append((too_add_2, root))
                            print('-', too_add_1)
                            print('-', too_add_2)

            if ',' in e.text:

                list_childs = [x for x in list(root.children) if
                               x.text in e.text.replace(',', ' ,').split() and x.pos_ == 'ADJ']
                print("Hijos:", list_childs)
                root_complete_no_coords = [x for x in list(root.subtree) if x.text in e.text.replace(',',
                                                                                                     ' ,').split() and x not in list_childs and x.pos_ != 'PUNCT' and x.pos_ != 'CCONJ']
                print("Núcleo:", root_complete_no_coords)

                for yuxt in list_childs:
                    to_add_yuxt = " ".join([i.text for i in list(yuxt.subtree) if
                                            i.text in e.text and i not in root_complete_no_coords and i.pos_ != 'PUNCT' and i.pos_ != 'CCONJ']) + " " + " ".join(
                        [i.text for i in root_complete_no_coords])
                    to_add.append((to_add_yuxt, root))
                    print('-', to_add_yuxt)


    else:
        if root:
            for t in e:
                if (((t.pos_ == 'ADV' or t.pos_ == 'CCONJ') and t.head.tag_ not in ['JJ', 'JJR', 'JJS', 'VBN',
                                                                                    'VBG']) or t.lemma_ == '•'):
                    to_delete = t.text
                    to_add.append((e.text.replace(to_delete, "").replace('however', "").strip(), root))
                else:
                    to_add.append((e.text.replace('however', ""), root))

    for tup in to_add:
        if tup[0] not in [x[0] for x in matches_clean_jj]:
            matches_clean_jj.append(tup)

# matches_clean_jj = delete_overlapping(matches_clean_jj)

# Saving results to txt
"""
with open('corpus/Medical/txt_all_noun_phrases.txt', 'w') as f_w:
    for e in matches_clean:
        f_w.write('- ' + e + '\n')

with open('corpus/Medical/txt_all_noun_phrases_plus_barePP.txt', 'w') as f_w:
    for e in matches_clean_pp:
        f_w.write('- ' + e + '\n')
"""

with open('corpus/Medical/txt_all_noun_phrases_adjectives.txt', 'w') as f_w:
    for tup in matches_clean_jj:
        f_w.write('- ' + tup[0] + ' / ' + tup[1].text + '\n')