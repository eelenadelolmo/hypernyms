# Testing different keyword extraction algorithms on the MedPix corpus

The corpus is available here: https://medpix.nlm.nih.gov/home

The original corpus is in the `venv/main/corpus/Medical/` folder, being the original versions `OutPretty.json` and `OutPretty.txt`.

The script `corpus_processing.py` creates the folder `venv/main/corpus/Medical/txt/` with one file for every case with its identifier as filename. The selected fields from the original cases are _exam_, _txFollowup_, _findings_, _diagnosis_, _ddx_, _history_ and _discussion_.

The script `frecuencies.py` modifies the output files in order to add the absolute frequency of every keaword in the whole corpus.



## Rake

- **Original paper**: https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents

- **Implementation**: https://pypi.org/project/rake-nltk/

RAKE, short for Rapid Automatic Keyword Extraction algorithm, is a domain independent keyword extraction algorithm which tries to determine key phrases in a body of text by analyzing the frequency of word appearance and its co-occurance with other words in the text.

RAKE is based on our observation that keywords frequently contain multiple words but rarely contain standard punctuation or stop words, such as the function words or other words with minimal lexical meaning. Co-occurrences of words within these candidate keywords are meaningful and allow us to identify word co-occurrence **without the application of an arbitrarily sized sliding window**.

The **input parameters** for the RAKE Algorithm comprise a list of **stop words** and a set of **phrase delimiters** and **word delimiters**. It uses stop words and phrase delimiters to partition the document into candidate keywords.

While RAKE has generated strong interest due to its ability to pick out highly specific terminology, **an interest was also expressed in identifying keywords that contain interior stop words**. To find these RAKE looks for pairs of keywords that adjoin one another at least twice in the same document and in the same order. A new candidate keyword is then created as a combination of those keywords and their interior stop words.

    - Word Frequency (freq(w)) --> favors words that occur frequently regardless of the number of words with which they co-occurred.
    - Word Degree (deg(w)) --> favors words that occur often and in longer candidates.
    - Ratio of degree to frequency (deg(w)/freq(w)) --> favors the words that predominately occur in longer candidate keywords.

The final score for each candidate keyword is calculated as the sum of its member word scores.



## Yake

- **Original paper**: https://www.sciencedirect.com/science/article/abs/pii/S0020025519308588?casa_token=NZfi-GmbK1gAAAAA:WC5tKprHpm5fy2askOGZsc_sFyqklbjNqUGrb7ipJZLTwgzqlPem_tqDDjy_rL_u44w2X_VVkkQ

- **Implementation**: https://github.com/LIAAD/yake

Light-weight **unsupervised** automatic keyword extraction method which rests on statistical text features extracted from **single documents** to select the most relevant keywords of a text. Our system does not need to be trained on a particular set of documents, nor does it depend on dictionaries, external corpora, text size, language, or domain.

    It has five main steps: 
    - Text pre-processing and candidate term identification: 
    - feature extraction: 
    - computing term score: 
    - n-gram generation and computing candidate keyword score: 
    - data deduplication and ranking: 

The algorithm receives a text and the following parameters as inputs: a window size w (to be used by one of the statistical features), the number of n-grams, the deduplication threshold ?? and the text language (for identification of the specific list of stopwords; note that tokens with fewer than three characters are also considered a stopword in our approach). 

Given a text, the algorithm begins by dividing it into sentences with the **segtok** rule-based sentence segmenter that also perferms the tokenisation (pypi.python.org/pypi/segtok).

Each term is characterized by a number of **statistical features**. These features comprise **TF** (term frequency), **offsets_sentences** (index of sentences where the terms occur), **TF_a** (term frequency of acronyms) and **TF_U** (term frequency of uppercase terms).

To compute every **term score**, we gather all the feature weights into a unique S(t) score. The smaller the value, the more significant the 1-gram term.

To form the list of candidate keywords, we consider a **sliding window** of size n, generating a contiguous sequence of terms ranging from 1-gram to n-grams, where n was experimentally evaluated, obtaining the best resunts for n=3 and n=2.

To compute the **score of an n-gram**, we begin by splitting each candidate into tokens and compute their S(t) into a formula to abstract the n-gram score. We evaluate whether the token is a stopword, since stopwords are given special treatment to mitigate the impact of applying their S(t), likely a high value, when put in context.

The final step is deciding if the **removal similar potential candidates** improves the ranking results. Two strings are considered similar if their distance similarity score is above a given threshold ??. Between two strings considered similar, we keep the most relevant one, that is, the one that has the lowest S(kw) score. Conversely, a candidate keyword is inserted into the list if no similarity between it and keywords already in the structure is found to be relevant. 

The final list of keywords is then given by **ascending order** of the S(kw) scores.



## Text rank

- **Original paper**: https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf

- **Implementation**: https://summanlp.github.io/textrank/

A **graph-based** ranking algorithm is a way of deciding on the importance of a vertex within a graph, by taking into account global information recursively computed from the entire graph, rather than relying only on local vertex-specific information. 

The basic idea implemented by a graph-based ranking model is that of _recommendation_: when **one vertex links to another one**, it is basically **casting a vote for that other vertex**. The higher the number of votes that are cast for a vertex, the higher the importance of the vertex.

The units to be ranked are therefore **sequences of one or more lexical units** extracted from text, and these represent the vertices that are added to the text graph. Any relation that can be defined between two lexical units is a potentially useful connection (edge) that can be added between two such vertices. This algorithm uses a **co-occurrence relation**: two vertices are connected if their corresponding lexical units co-occur **within a window of maximum words**, set anywhere from 2 to 10 words. 

The edges the graph can be restricted with **syntactic filters**, which select only co-occurrences of lexical units with a certain PoS tag. The best results was observed for nouns and adjectives only.

First, the text is tokenized, and PoS tagged. To avoid excessive growth of the graph size by adding all possible combinations of sequences consisting of more than one lexical unit, we consider only **single words as candidates for addition to the graph**, with multi-word keywords being eventually reconstructed in the post-processing phase.

Next, all lexical units that pass the syntactic filter are added to the graph, and an **edge** is added between those **lexical units that co-occur** within a n window of words.

Once a final score is obtained for each vertex in the graph, vertices are sorted in reversed order of their score, and the **top vertices in the ranking** are retained for post-processing. 

The **number of keywords** extracted depends on the size of the text and is set to a third of the number of vertices in the graph.

During post-processing, all lexical units selected as potential keywords by the TextRank algorithm are marked in the text, and **sequences of adjacent keywords are collapsed** into a multiword keyword.




## Topic rank

- **Original paper**: https://www.aclweb.org/anthology/I13-1062.pdf

- **Implementation**: https://boudinfl.github.io/pke/build/html/unsupervised.html#topicrank

A **graph-based** keyphrase extraction method that relies on a **topical representation** of the document. Candidate **keyphrases are clustered** into topics and used as vertices in a complete graph. A graph-based ranking model is applied to assign a significance score to each topic. Keyphrases are then generated by selecting **a candidate from each of the top ranked topics**.

Our approach has several **advantages over TextRank**. Intuitively, ranking topics instead of words is a more straightforward way to identify the set of keyphrases that **covers the main topics** of a document. Besides, clustering keyphrase candidates into topics also **eliminates redundancy** while reinforcing edges.

We propose to group similar noun phrases as a single entity, a topic. We consider that two keyphrase candidates are similar if they have **at least 25% of overlapping words**. Keyphrase candidates are stemmed to reduce their inflected word forms into root forms.

To automatically **group similar candidates into topics**, we use a Hierarchical Agglomerative Clustering (HAC) algorithm. 

The topic vectices and connected with all the others, using the **TextRank algorithm** for their ranking. 

To find the **candidate that best represents a topic**, we propose three strategies. 

    - Selecting the first mention. 
    - Selecting the most frequent mention. 
    - Selecting the centroid of the cluster, which is the most similar to the other candidates of the cluster.




## KeyBERT

- **Original paper**: 

- **Implementation**: https://github.com/MaartenGr/KeyBERT


Uses BERT-embeddings and simple cosine similarity to find the **sub-phrases in a document that are the most similar to the document itself**.

You can set `keyphrase_ngram_range` to set the length of the resulting keywords (1,15 in our script).

You can select any model from `sentence-transformers` here (https://www.sbert.net/docs/pretrained_models.html) and pass it through KeyBERT. 'distilbert-base-nli-mean-tokens' or 'xlm-r-distilroberta-base-paraphrase-v1' as they have shown great performance in semantic similarity and paraphrase identification respectively.

The results are ordered by its similarity measure.

Output in the `keybert/keybert` folder.

- To **diversify** the results:

    Max Sum Similarity: `model.extract_keywords(doc, keyphrase_ngram_range=(3, 3), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=5)`
    Output in the `keybert/keybert_maxSum` folder.
    
    Maximal marginal relevance: `model.extract_keywords(doc, keyphrase_ngram_range=(3, 3), stop_words='english', use_mmr=True, diversity=0.7)`
    Output in the `keybert/keybert_maxMargRelevance` folder.

- **Multiple documents**:

    There is an option to extract keywords for multiple documents that is faster than extraction for multiple single documents. However, this method assumes that you can keep the word embeddings for all words in the vocabulary in memory which might be troublesome.
    
    You can set the `min_df` paramater to specify the minimum document frequency of a word across all documents if keywords for multiple documents need to be extracted.

    

## TF-IDF

- **Original paper**: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.115.8343&rep=rep1&type=pdf

- **Implementation**: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html#examples-using-sklearn-feature-extraction-text-tfidfvectorizer


TF-IDF is a numerical statistic that is intended to reflect **how important a word is to a document in a collection or corpus**. 

The tf???idf value for a word **increases** proportionally **appearances of the word in the text and is **offset by the number of documents** where it appears.

The output of the original formula is in the `tf_idf/tf_idf` folder. 

We have also tested the **scikit-learn implementation** (TfidfVectorizer). Its outputis in the `tf_idf/tf_idf_sklearn` folder. 

The main difference between these two lies in an **extra normalization step** carried out in the scikit-learn known as Euclidean normalization. Besides, the scikit-learn implementation performs the **addition of unitary constants in the denominator and numerator for the computation of the IDF** in order to avoid zero divisions.


## Noun phrases + absolute frequencies 

Documentation from: https://buildmedia.readthedocs.org/media/pdf/textacy/latest/textacy.pdf

**patterns** ??? One or multiple patterns to match against doclike using a spacy.matcher.Matcher.

If `List[dict]` or `List[List[dict]]`, each pattern is specified as attr: value pairs per token, with optional quantity qualifiers:

    [{"POS": "NOUN"}] matches singular or plural nouns, like ???friend??? or ???enemies???
    [{"POS": "PREP"}, {"POS": "DET", "OP": "?"}, {"POS":"ADJ", "OP": "?"}, {"POS": "NOUN", "OP": "+"}] matches prepositional phrases, like ???in the future??? or ???from the distant past???
    [{"IS_DIGIT": True}, {"TAG": "NNS"}] matches numbered plural nouns, like ???60 seconds??? or ???2 beers???
    [{"POS": "PROPN", "OP": "+"}, {}] matches proper nouns and whatever word follows them, like ???Burton DeWilde yaaasss???

If `str` or `List[str]`, each pattern is specified as one or more per-token patterns separated by whitespace where attribute, value, and optional quantity qualifiers are delimited by colons.

Note that boolean and integer values have special syntax ??? ???bool(val)??? and ???int(val)???, respectively ??? and that wildcard tokens still need a colon between the (empty) attribute and value strings.

- `"POS:NOUN"` matches singular or plural nouns
- `"POS:PREP POS:DET:? POS:ADJ:? POS:NOUN:+"` matches prepositional phrases
- `"IS_DIGIT:bool(True) TAG:NNS"` matches numbered plural nouns
- `"POS:PROPN:+ :"` matches proper nouns and whatever word follows them

Also note that these pattern strings don???t support spaCy v2.1???s ???extended??? pattern syntax; if you need such complex patterns, it???s probably better to use a `List[dict]` or `List[List[dict]]`, anyway.

The **patterns matched** are:

    pattern_np = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}]
    pattern_pnp = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"*"}, {"POS": "PROPN", "OP":"+"}, {"POS": "NOUN", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}]
    pattern_np_pp = [{"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADP"}, {"POS": "DET", "OP":"?"}, {"POS": "NUM", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"TEXT": ",", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "NOUN", "OP":"+"}, {"POS": "ADV", "OP":"*"}, {"POS": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"TAG": "VBN", "OP":"*"}, {"POS": "CONJ", "OP":"*"}, {"POS": "ADV", "OP":"*"}, {"POS": "ADV", "OP":"*"}]

The output of the noun phrases not containing prepositional phrases are in the `txt_all_noun_phrases.txt` file. 
The output of the noun phrases (not containing proper nouns) containing prepositional phrases are in the `txt_all_noun_phrases_pp.txt` file. 
