import io
import os
import re
import json
import codecs
import unicodedata
from os.path import splitext


def preprocessing(src):
    with io.open(src, 'r', encoding='utf-8', errors='ignore') as temp:
        text = temp.read()
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        # Remove non-letter characters and underscores
        text = re.sub(r'[^A-Za-zÀ-ÿ ]+', '', text.lower())
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text


def count_len(src):
    return len(preprocessing(src))


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


def calculate_score(ngrams_input, ngrams_lang, corpus_len, lang_len):
    overlap = set(ngrams_input.keys()) & set(ngrams_lang.keys())
    overlap_freq_input = sum([ngrams_input[ngram] for ngram in overlap])
    overlap_freq_lang = sum([ngrams_lang[ngram] for ngram in overlap])
    total_freq_input = sum(ngrams_input.values())
    total_freq_lang = sum(ngrams_lang.values())

    factor = 1 - (lang_len / corpus_len)

    score = overlap_freq_input / total_freq_input * overlap_freq_lang / total_freq_lang * factor
    return score


def apply_laplace_smoothing(language, file=0):
    V = calculate_vocabulary_size('../assets/raw/nld.txt')
    with open('../assets/json/' + language + '_3.json', 'r') as f:
        trigram_counts = json.load(f)
    with open('../assets/json/' + language + '_2.json', 'r') as f:
        bigram_counts = json.load(f)

    trigram_probs = {}
    for trigram in trigram_counts:
        bigram = trigram[:2]
        count_tri = trigram_counts[trigram]
        count_bi = bigram_counts[bigram]
        prob = (count_tri + 1) / (count_bi + V)
        trigram_probs[trigram] = prob
    if file == 1:
        with open('../assets/chances/' + language + '.json', "w", encoding="utf-8") as f:
            json.dump(trigram_probs, f)
    return trigram_probs


def calculate_vocabulary_size(text_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    bigrams = set(zip(text, text[1:]))
    return len(bigrams)


languages = {
    'nld': 'nld.txt',
    'eng': 'eng.txt',
    'ger': 'ger.txt',
    'fra': 'fra.txt',
    'ita': 'ita.txt',
    'spa': 'spa.txt',
}


def detect_language(input_text):
    trigrams = make_ngrams(input_text, 3)
    language_probabilities = {}
    for filename in os.listdir('../assets/json/'):
        if filename.endswith('_3.json'):
            language = filename.split('_')[0]
            trigram_probs = apply_laplace_smoothing(language)
            probability = 1
            for trigram in trigrams:
                if trigram in trigram_probs:
                    probability *= trigram_probs[trigram]
                else:
                    probability *= 1e-10  # use a small probability for unseen trigrams
            language_probabilities[language] = probability
    return sorted(language_probabilities.items(), key=lambda x: x[1], reverse=True)



def calculate(text):
    bigrams_input = make_ngrams(text, 2)
    trigrams_input = make_ngrams(text, 3)

    corpus_len = 0
    for lang, filename in languages.items():
        corpus_len += count_len(f"../assets/raw/{filename}")

    scores = {}
    scores_list = []
    for lang, filename in languages.items():
        bigrams = make_ngrams_from_file(f"../assets/raw/{filename}", 2)
        trigrams = make_ngrams_from_file(f"../assets/raw/{filename}", 3)
        score_bigrams = calculate_score(bigrams_input, bigrams, corpus_len,
                                        count_len(f"../assets/raw/{filename}"))
        score_trigrams = calculate_score(trigrams_input, trigrams, corpus_len,
                                         count_len(f"../assets/raw/{filename}"))
        scores[lang] = (score_bigrams + score_trigrams) / 2
        scores_list.append([lang, score_bigrams, score_trigrams, (score_bigrams + score_trigrams) / 2])

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print(f"De taal {sorted_scores[0][0]} is gedetecteerd: {sorted_scores[0][1]} (bi: {score_bigrams} + tri: {score_trigrams}")
    for lang, score in sorted_scores[1:]:
        for a in scores_list:
            if lang in a:
                print(f"{lang}: {score} (bi: {a[1]} + tri: {a[2]}")


def process_input():
    print("Hoe wil je het algoritme testen?")
    print("0 - Zelf tekst invoeren")
    print("1 - Nederlands")
    print("2 - Engels")
    print("3 - Duits")
    print("4 - Frans")
    print("5 - Italiaans")
    print("6 - Spaans")

    selection = int(input("Geef je input: "))
    print("")
    text = ""

    match selection:
        case 0:
            text = input()
        case 1:
            text = "Hallo ik ben een man die kaas eet en water drinkt"
        case 2:
            text = "Hello I am a man who eats cheese and drinks water"
        case 3:
            text = "Hallo, ich bin ein Mann, der Käse isst und Wasser trinkt"
        case 4:
            text = "Bonjour je suis un homme qui mange du fromage et boit de l'eau"
        case 5:
            text = "Ciao sono un uomo che mangia formaggio e beve acqua"
        case 6:
            text = "Hola soy un hombre que come queso y bebe agua"
        case other:
            print("Probeer het opnieuw")
    print("Input: " + text)
    print("Versie A")
    calculate(text)
    print("------------------")
    print("Versie B")
    print(detect_language(text))

    print("")
    print("")
    process_input()


langs = ['eng', 'fra', 'ita', 'nld', 'spa', 'ger']

process_input()
