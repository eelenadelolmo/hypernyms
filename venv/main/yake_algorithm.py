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





from yake import KeywordExtractor
kw_extractor = KeywordExtractor(lan="en", n=1, top=5)

for j in range(len(array_text)):
    keywords = kw_extractor.extract_keywords(text=array_text[j])
    keywords = [x for x, y in keywords]
    print("Keywords of article", str(j+1), "\n", keywords)