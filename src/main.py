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

def calculate_score(ngrams_input, ngrams_lang):
    overlap = set(ngrams_input.keys()) & set(ngrams_lang.keys())
    #total_overlap_count = sum([((ngrams_input[ngram] + ngrams_lang[ngram]) / 2) for ngram in overlap])
    total_ngrams_count_input = sum(ngrams_input.values())
    total_ngrams_count_lang = sum(ngrams_lang.values())

    # Calculate the maximum a posteriori (MAP)
    score = sum([ngrams_input[ngram] for ngram in overlap]) / total_ngrams_count_input * sum([ngrams_lang[ngram] for ngram in overlap]) / total_ngrams_count_lang
    return score

input = "Today I feel like doing nothing"
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
    score_bigrams = calculate_score(bigrams_input, bigrams)
    score_trigrams = calculate_score(trigrams_input, trigrams)
    scores[lang] = score_trigrams

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print(f"De taal {sorted_scores[0][0]} is gedetecteerd: {sorted_scores[0][1]}")
for lang, score in sorted_scores[1:]:
    print(f"{lang}: {score}")
