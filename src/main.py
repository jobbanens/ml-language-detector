import io
import os
import re
import json
import codecs
from os.path import splitext

def preprocessing(src):
    with io.open(src, 'r', encoding='utf-8', errors='ignore') as temp:
        return re.sub("[\n]+", ' ', (re.sub("[^A-Za-zÀ-Ÿ\n_ ']+", '', temp.read()).lower()))

def make_ngrams_from_file(src, n):
    # Preprocess the source file
    src = preprocessing(src)

    # Make list of ngrams
    n_grams = []
    for i in range(len(src)):
        n_grams.append(src[i: i + n])

    # Count the frequency of the ngrams
    dict = {}
    for i in n_grams:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1

    return dict

def make_ngrams(src, n):
    # Preprocess the source file
    src = re.sub("[\n]+", ' ', (re.sub("[^A-Za-zÀ-Ÿ\n_ ']+", '', src.lower())))

    # Make list of ngrams
    n_grams = []
    for i in range(len(src)):
        n_grams.append(src[i: i + n])

    # Count the frequency of the ngrams
    dict = {}
    for i in n_grams:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1

    return dict

def process_files(n):
    # For every raw file, create ngrams and save to a json file
    for file in os.listdir('../assets/raw/'):
        print(file)
        ngrams = make_ngrams_from_file('../assets/raw/' + file, n)
        json_object = json.dumps(ngrams)
        with codecs.open('../assets/json/' + splitext(file)[0] + '_' + str(n) + '.json', 'w+', 'utf-8') as f:
            f.write(json_object)

def calculate_map(ngram1, ngrams2):
    overlap = set(ngram1.keys()) & set(ngrams2.keys())
    total_overlap_count = sum([min(ngram1[g], ngrams2[g]) for g in overlap])
    total_bigrams1_count = sum(ngram1.values())
    total_bigrams2_count = sum(ngrams2.values())

    # Calculate the maximum a posteriori (MAP)
    map = (total_overlap_count + 1) / (total_bigrams1_count + len(ngram1.keys()))
    return map

input = "Ciao sono una bambina con un pezzo di formaggio"
bigrams_input = make_ngrams(input, 2)
trigrams_input = make_ngrams(input, 3)

languages = {
    'nld': 'nld.txt',
    'eng': 'eng.txt',
    'ger': 'ger.txt',
    'fra': 'fra.txt',
    'ita': 'ita.txt',
    'cat': 'cat.txt',
}

scores = {}
for lang, filename in languages.items():
    bigrams = make_ngrams_from_file(f"../assets/raw/{filename}", 2)
    trigrams = make_ngrams_from_file(f"../assets/raw/{filename}", 3)
    score_bigrams = calculate_map(bigrams_input, bigrams)
    score_trigrams = calculate_map(trigrams_input, trigrams)
    scores[lang] = score_bigrams + score_trigrams / 2

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print(f"De taal {sorted_scores[0][0]} is gedetecteerd: {sorted_scores[0][1]}")
for lang, score in sorted_scores[1:]:
    print(f"{lang}: {score}")
