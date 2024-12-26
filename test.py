import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# nltk.download('stopwords')
# nltk.download('punkt')

def summary(text):
    stop_words = set(stopwords.words('indonesian'))
    words = word_tokenize(text)

    freq_table = {}
    for word in words:
        word = word.lower()
        if word not in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1
    
    sentences = sent_tokenize(text)
    sentence_value = {}

    for sentence in sentences:
        for word_value in freq_table:
            if word_value in sentence.lower():
                if sentence[:12] in sentence_value:
                    sentence_value[sentence[:12]] += freq_table[word_value]
                else:
                    sentence_value[sentence[:12]] = freq_table[word_value]
    
    sum_values = 0
    for entry in sentence_value:
        sum_values += sentence_value[entry]
    
    average = int(sum_values / len(sentence_value))

    summary = ''
    for sentence in sentences:
        if (sentence[:12] in sentence_value) and (sentence_value[sentence[:12]] > (1.2 * average)):
            summary += sentence + ' '
    
    return summary

teks = input("Masukan teks: ")
print("Hasil : ", summary(teks))

