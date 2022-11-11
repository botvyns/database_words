from collections import defaultdict
import pymorphy2
import string
import tokenize_uk

lemma_info = defaultdict(list)

morph = pymorphy2.MorphAnalyzer(lang="uk")

with open("tales.txt", "r", encoding="utf-8") as f:
    text = f.read()

# tokenize text to words

tokenized_words = [
    word.lower() for word in tokenize_uk.tokenize_words(text) if word.isalpha()
]

# fill lemma_info where key is lemmatized word and values are list [pos, [inflections]]

for w in tokenized_words:
    lemma_info[morph.parse(w)[0].normal_form] = (
        morph.parse(w)[0].tag.POS,
        [inf[0] for inf in morph.parse(w)[0].lexeme],
    )

# uncomment lines below to see keys and values of lemma_info

# for k, v in lemma_info.items():
#     print(k, '----->', v)
