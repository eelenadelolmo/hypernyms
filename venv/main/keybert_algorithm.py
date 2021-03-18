import trafilatura
array_links = [
    "https://en.wikipedia.org/wiki/Coronavirus_disease_2019",
    "https://en.wikipedia.org/wiki/Recession",
    "https://en.wikipedia.org/wiki/Vienna",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Graph_database"
]
array_text = []
for l in array_links:
    html = trafilatura.fetch_url(l)
    text = trafilatura.extract(html)
    text_clean = text.replace("\n", " ").replace("\'", "")
    array_text.append(text_clean[0:5000])






from keybert import KeyBERT
kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
for j in range(len(array_text)):
    keywords = kw_extractor.extract_keywords(array_text[j], keyphrase_ngram_range=(1,4), stop_words='english')
    print("Keywords of article", str(j+1), "\n", keywords)