import nltk
# from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from heapq import nlargest
import re
import PyPDF2

myfile = open('file.pdf', mode='rb')
pdf_reader = PyPDF2.PdfReader(myfile)

teks_pdf = []
# teks_pdf = {}
for idx, page_num in enumerate(range(len(pdf_reader.pages))):
    page_obj = pdf_reader.pages[page_num]
    teks = page_obj.extract_text()
    teks_pdf.append(teks)

artikel = ' '.join(teks_pdf)
artikel = artikel.replace('KEAMANAN DATA DAN SISTEM INFORMASI', '')
artikel = artikel.replace('TEKNIK INFOMRAMTIKA', '')

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

    sorted_kalimat = sorted(kalimat_weight, key=lambda item: item[1], reverse=True)
    new_summary_text = sorted_kalimat[0:select_length]

    new_kalimat_weight = dict()
    for kal in kalimat_weight:
        if kal in new_summary_text:
            new_kalimat_weight[kal] = kalimat_weight[kal]

    summary = list(new_kalimat_weight)

    final_summary = [word for word in summary]
    summary = ' '.join(final_summary)

    # print(summary)
    return summary

tahap1 = get_summary(artikel, 0.3)
tahap2 = get_summary(tahap1, 0.6)
print(tahap2)