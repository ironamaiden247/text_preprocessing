import csv
import re
import nltk.tokenize
import nltk.corpus
import nltk.stem

# Parts of speech: NOUN, VERB, ADJ, ADV == 'n', 'v', 'a', 'r'
pos_to_lemma = {
    'NN': 'n',
    'NNS': 'n',
    'VB': 'v',
    'VBG': 'v',
    'JJ': 'a',
    'RB': 'r',
}


class ReviewInstance:
    """Object representing a single user review"""

    def __init__(self, rating, sentence):
        stop_words = set(nltk.corpus.stopwords.words('english'))

        self.rating = rating
        self.sentence = sentence
        self.has_noun = False

        self.tokens = []
        self.unfiltered_tokens = nltk.word_tokenize(sentence)
        speech_tags = nltk.pos_tag(self.unfiltered_tokens)
        lemmatizer = nltk.WordNetLemmatizer()
        for i, t in enumerate(self.unfiltered_tokens):
            # t = re.sub('[^a-z0-9]+', '', t)
            t = re.sub(r'\d+', "", t)
            t = re.sub(r'[^\w\s]', '', t)
            if t not in stop_words:
                part_of_speech = speech_tags[i][1]  # part of speech for t
                if part_of_speech == 'NN' or part_of_speech == 'NNS':
                    self.has_noun = True
                lemmatized = lemmatizer.lemmatize(t, pos=pos_to_lemma.get(part_of_speech, 'n'))
                # print(part_of_speech + ' -- ' + t + ' -- ' + lemmatized)
                self.tokens.append(lemmatized)

        # self.sentiment = {'pos': 0, 'neg': 0, 'neu': 0}

    def print(self):
        print("Rating: " + self.rating + " -- Sentence: " + self.sentence)


def read_reviews(path_to_csv, split_sentences):
    nltk.download('stopwords')
    review_instances = []
    with open(path_to_csv, newline='', encoding='utf-8') as csvfile:
        review_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(review_reader, None)  # Skip csv headers
        for row in review_reader:
            # print(row)
            comment = row[1]
            rating = row[0]

            sentences = nltk.sent_tokenize(comment.lower()) if split_sentences else [comment.lower()]
            for s in sentences:
                review = ReviewInstance(rating, s)
                if review.has_noun:
                    review_instances.append(review)

    return review_instances


def export(review_list, path_to_csv):
    with open(path_to_csv, 'w', newline='', encoding='utf-8') as out_file:
        review_writer = csv.writer(out_file, delimiter=',', quotechar='"')
        for r in review_list:
            review_writer.writerow([''] + [r.rating] + [' '.join(r.tokens)])

'''
In 'main.py' call
reviews_unified = data_preprocessing.read_reviews("C:\\Users\\malsa876\\Desktop\\PyTest\\DATASET\\my-tracks-reviews.csv", False)
data_preprocessing.export(reviews_unified, "C:\\Users\\malsa876\\Desktop\\PyTest\\DATASET\\mytracks_exported_unified.csv")
'''