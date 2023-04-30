import stem.process
import requests
from bs4 import BeautifulSoup
import logging
import requests
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest


def scrap(t):
    logging.getLogger().setLevel(logging.INFO)
    tor_cmd = r"C:\Users\kaushal\OneDrive\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe"
    config_options = {"SocksPort": "9050", "Log": "notice stdout"}
    import subprocess
    # subprocess.call(['taskkill', '/f', '/im', 'tor.exe'])
    tor_process = stem.process.launch_tor_with_config(tor_cmd=tor_cmd, config=config_options)
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }
    response = session.get(t)
    tor_process.kill()
    return response

def summarize(text, n):
    sentences = sent_tokenize(text)

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in stop_words]
    freq_dist = nltk.FreqDist(words)
    scores = {}
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence)
        words = [word for word in words if word.lower() not in stop_words]
        score = sum([freq_dist[word] for word in words])
        scores[i] = score
    top_sentences = nlargest(n, scores, key=scores.get)
    summary = [sentences[j] for j in sorted(top_sentences)]
    summary = ' '.join(summary)
    return summary


def match(summary):
    li=[]
    with open('dataForSearch.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            li.append(row)
    if substring in string:
    words_to_compare=summary
    matching_words = [word for word in li if word in words_to_compare]
    matching_word_count = len(matching_words)
    percentage_matching = (matching_word_count / len(li)) * 100

    return "{:.2f}%".format(percentage_matching)

# soup = BeautifulSoup(scrap("http://freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion").content, 'html.parser')
# urls = []
# for link in soup.find_all('a'):
#     d=link.get('href')
#     if "http" in d:
#         print(d)
#         urls.append(d)

# with open('links.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for url in urls:  
#         writer.writerow([url])


with open('links.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        soup = BeautifulSoup(scrap(row[0]).content, 'html.parser')
        text_tags = soup.get_text()
        print(text_tags)
        summary = summarize(text_tags, 2)
        print(row,"Match",match(summary))
        with open('Output_links.csv', 'w', newline='') as f:
            writer = csv.writer(f) 
            writer.writerow(row)