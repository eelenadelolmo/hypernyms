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




from summa import keywords
for j in range(len(array_text)):
    print("Keywords of article", str(j+1), "\n", (keywords.keywords(array_text[j], words=5)).split("\n"))