__author__ = 'Sadir'

import csv
import re

class Dictionary(object):

    categories = ["condAct", "condCom", "condLog", "condPrp", "condPrs", "loct", "propEst", "propFac", "propInt", "sociMea", "sociPpl", "sociPrs", "sociShr", "sociTlk", "isGuest", "isHost"]
    words = {}

    def __init__(self, path):
        with open(path) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                self.words[row["word"]] = self.categories.index(row["category"])

    def showdict(self):
        print(self.words)

    def getSentenceStats(self, sentence):

        dict = {}
        for cat in self.categories:
            dict[cat] = 0

        tokens = list(self.tokenize(sentence))
        for token in tokens:
            if token in self.words:
                word_category = self.categories[self.words[token]]
                dict[word_category] += 1

        return dict

    def tokenize(self, text):
        text = text.lower()
        for match in re.finditer(r'\w+', text, re.UNICODE):
            yield match.group(0)
'''
def getScores(Dictio, text):
    word_count = len(re.findall("[a-zA-Z_]+", text))
    all_scores = Dictio.getSentenceStats(text)
    scores = {}
    profession = all_scores['condAct'] + all_scores['condCom'] + all_scores['condLog'] + all_scores['condPrp'] + all_scores['condPrs']
    location = all_scores['loct']
    property = all_scores['propEst'] + all_scores['propFac'] + all_scores['propInt']
    social = all_scores['sociMea'] + all_scores['sociPpl'] + all_scores['sociPrs'] + all_scores['sociShr'] + all_scores['sociTlk']
    print(profession, location, property, social)

    if (word_count!=0):
        scores['prof'] = profession / word_count
        scores['loc'] = location / word_count
        scores['prop'] = property / word_count
        scores['soc'] = social / word_count

    else:
        scores['prof'] = -1
        scores['loc'] = -1
        scores['prop'] = -1
        scores['soc'] = -1

    if (social + profession) == 0:
        scores['soc_rel'] = -1
    else:
        scores['soc_rel'] = social / (social + profession)
    #print(scores)

    return scores
    '''

path = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/dictionaries/mydict/mydict.tsv"
dict = Dictionary(path)
#print(getScores(dict, "Guy is a friendly, warm, reliable and easy- going host who knows (and loves!) everything about London and who shares so many stories and experiences. Make sure to ask about the must-go London pubs and places to eat!"))
print(dict.getSentenceStats("Guy is a friendly, warm, reliable and easy- going host who knows (and loves!) everything about London and who shares so many stories and experiences. Make sure to ask about the must-go London pubs and places to eat!"))