import re
from collections import Counter
import liwc

#needed for parser
dictionary_path= "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/dictionaries/LIWC2007_English080730.dic"
parse, category_names = liwc.load_token_parser(dictionary_path)

def getScores(text):
    #print("Text is: ", text)
    #review_tokens = tokenize(text)
    review_tokens = tokenize(text)
    for token in review_tokens:
        print(token, [value for value in list(parse(token)) if value in ["ppron", "ipron", "affect"]])
    category_counts = Counter(category for token in review_tokens for category in parse(token))
    word_count = len(re.findall("[a-zA-Z_]+", text))
    #print("word count is: ", word_count)
    scores = {}
    personal = category_counts['ppron']
    print("personal count: ", personal)

    impersonal = category_counts['ipron']
    print("impersonal count: ", impersonal)

    affect = category_counts['affect']
    print("affect count: ", affect)

    if (word_count!=0):
        scores['affect/tot'] = affect / word_count
        scores['pers/tot'] = personal / word_count
        scores['impers/tot'] = impersonal / word_count
    else:
        scores['affect/tot'] = -1
        scores['pers/tot'] = -1
        scores['impers/tot'] = -1

    if (personal+impersonal) == 0:
        scores['pers/(pers+impers)'] = -1
    else:
        scores['pers/(pers+impers)'] = personal / (personal+impersonal)
    #print(scores)

    return scores

def tokenize(text):
    text = text.lower()
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)


print(getScores("Never have I been as pleasantly surprised in an accommodation as this apartment in London. It is perfect for staying in the London Docklands area. The apartment is clean, has everything one could want to cook a meal, is extremely conveniently located with a 5 minute walk to the Jubilee line, as well as the DLR stations. The area has a multitude of restaurants and shopping facilities"))