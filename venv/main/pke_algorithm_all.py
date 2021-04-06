import pke


# Text of length 7620447 exceeds maximum of 1000000. The parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input. This means long texts may cause memory allocation errors. If you're not using the parser or NER, it's probably safe to increase the `nlp.max_length` limit. The limit is in number of characters, so you can check whether your inputs are too long by checking `len(text)`.
all = 'corpus/Medical/txt_all.txt'
all_kw = 'corpus/Medical/txt_all_pke_topic_rank.txt'

with open(all) as f:
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=all, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keywords = extractor.get_n_best(n=10)

with open(all_kw, 'w') as f_w:
    for keyword in keywords:
        f_w.write('- ' + keyword + '\n')
