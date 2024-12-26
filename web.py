import urllib.request
import requests
import bs4 as BeautifulSoup
import nltk
# from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from heapq import nlargest
import re

url = 'https://konsultasisyariah.com/41335-bolehkah-wanita-berjilbab-tampil-imut-genit-dan-manja-di-medsos.html'
response_post = requests.get(url)
response_soup = BeautifulSoup.BeautifulSoup(response_post.text, 'html.parser')
all_paragraf = response_soup.find_all('p')
artikel = ''
for p in all_paragraf:
    artikel += p.text + ' '

artikel = ' '.join(re.findall("[a-zA-Z0-9,.\"'()\[\]:/;?&`!\’\“\-\+\=]+", artikel))
artikel = artikel.replace('KonsultasiSyariah.com', '')
# print(artikel)
# exit()

def get_summary(artikel, panjang=0.3):
    from string import punctuation

    stop_words = stopwords.words('indonesian')
    punctuation = punctuation + '\n'

    tokens = word_tokenize(artikel)
    # print(token)
    # exit()
    # print(stop_words)
    # print(punctuation)
    frekuensi_kata = {}
    for word in tokens:
        if word.lower() not in stop_words:
            if word.lower() not in punctuation:
                if word not in frekuensi_kata.keys():
                    frekuensi_kata[word] = 1
                else:
                    frekuensi_kata[word] += 1

    # print(frekuensi_kata)
    max_frekuensi = max(frekuensi_kata.values())
    # print(max_frekuensi)

    for word in frekuensi_kata.keys():
        frekuensi_kata[word] = frekuensi_kata[word]/max_frekuensi


    token_kalimat = sent_tokenize(artikel)
    kalimat_weight = dict()
    for kalimat in token_kalimat:
        kata_dalam_kalimat = (len(word_tokenize(kalimat)))
        kata_dalam_kalimat_tanpa_stopwords = 0
        for word_weight in frekuensi_kata:
            if word_weight in kalimat.lower():
                kata_dalam_kalimat_tanpa_stopwords += 1
                if kalimat in kalimat_weight:
                    kalimat_weight[kalimat] += frekuensi_kata[word_weight]
                else:
                    kalimat_weight[kalimat] = frekuensi_kata[word_weight]

    select_length = int(len(kalimat_weight)*panjang)

    summary = nlargest(select_length, kalimat_weight, key = kalimat_weight.get)
    # print(kalimat_weight)
    # exit()

    final_summary = [word for word in summary]
    summary = ' '.join(final_summary)

    # print(summary)
    return summary

tahap1 = get_summary(artikel, 0.3)
tahap2 = get_summary(tahap1, 0.6)
print(tahap2)