import re
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

input = "io sono una ragazza"
bigrams_input = make_ngrams(input, 2)
trigrams_input = make_ngrams(input, 3)

nld = "Het liefst was Rex nu toch echt doorgereden, maar het was niet het moment om haar goede bedoelingen ongebruikt te laten"
bigrams_nld = make_ngrams(nld, 2)
trigrams_nld = make_ngrams(nld, 3)

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


print(str(total_score_nld))
