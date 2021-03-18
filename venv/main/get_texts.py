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