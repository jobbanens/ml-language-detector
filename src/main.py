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

#process_files(2)
#process_files(3)

input = "Ciao sono una bambina con un pezzo di formaggio"
bigrams_input = make_ngrams(input, 2)
trigrams_input = make_ngrams(input, 3)

bigrams_nld = make_ngrams_from_file('../assets/raw/nld.txt', 2)
trigrams_nld = make_ngrams_from_file('../assets/raw/nld.txt', 3)

bigrams_eng = make_ngrams_from_file('../assets/raw/eng.txt', 2)
trigrams_eng = make_ngrams_from_file('../assets/raw/eng.txt', 3)

bigrams_ger = make_ngrams_from_file('../assets/raw/ger.txt', 2)
trigrams_ger = make_ngrams_from_file('../assets/raw/ger.txt', 3)

bigrams_fra = make_ngrams_from_file('../assets/raw/fra.txt', 2)
trigrams_fra = make_ngrams_from_file('../assets/raw/fra.txt', 3)

bigrams_ita = make_ngrams_from_file('../assets/raw/ita.txt', 2)
trigrams_ita = make_ngrams_from_file('../assets/raw/ita.txt', 3)

bigrams_cat = make_ngrams_from_file('../assets/raw/cat.txt', 2)
trigrams_cat = make_ngrams_from_file('../assets/raw/cat.txt', 3)

def calculate_map(ngram1, ngrams2):
    overlap = set(ngram1.keys()) & set(ngrams2.keys())
    total_overlap_count = sum([min(ngram1[g], ngrams2[g]) for g in overlap])
    total_bigrams1_count = sum(ngram1.values())
    total_bigrams2_count = sum(ngrams2.values())

    # Calculate the maximum a posteriori (MAP)
    map = (total_overlap_count + 1) / (total_bigrams1_count + len(ngram1.keys()))
    return map

score_bigrams_nld = calculate_map(bigrams_input, bigrams_nld)
score_trigrams_nld = calculate_map(trigrams_input, trigrams_nld)
total_score_nld = score_bigrams_nld + score_trigrams_nld

score_bigrams_eng = calculate_map(bigrams_input, bigrams_eng)
score_trigrams_eng = calculate_map(trigrams_input, trigrams_eng)
total_score_eng = score_bigrams_eng + score_trigrams_eng

score_bigrams_ger = calculate_map(bigrams_input, bigrams_ger)
score_trigrams_ger = calculate_map(trigrams_input, trigrams_ger)
total_score_ger = score_bigrams_ger + score_trigrams_ger

score_bigrams_fra = calculate_map(bigrams_input, bigrams_fra)
score_trigrams_fra = calculate_map(trigrams_input, trigrams_fra)
total_score_fra = score_bigrams_fra + score_trigrams_fra

score_bigrams_ita = calculate_map(bigrams_input, bigrams_ita)
score_trigrams_ita = calculate_map(trigrams_input, trigrams_ita)
total_score_ita = score_bigrams_ita + score_trigrams_ita

score_bigrams_cat = calculate_map(bigrams_input, bigrams_cat)
score_trigrams_cat = calculate_map(trigrams_input, trigrams_cat)
total_score_cat = score_bigrams_cat + score_trigrams_cat

scores = {
    'nld': total_score_nld,
    'eng': total_score_eng,
    'ger': total_score_ger,
    'fra': total_score_fra,
    'ita': total_score_ita,
    'cat': total_score_cat,
}

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("De taal " + str(sorted_scores[0][0]) + " is gedetecteerd: " + str(sorted_scores[0][1]))
for score in sorted_scores[1:]:
    print(f"{score[0]}: {score[1]}")
