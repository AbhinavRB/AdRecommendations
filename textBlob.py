from textblob import TextBlob 

string = "SAD DEMISE \r\nSri MANHARLAL P SHETH \r\nPeacefully passed away \r\non 28.12.2015. \r\nA great soul serves \r\neveryone all the time. A \r\ngreat soul never dies."

string = ''' HONDDA
The Power of Dreams
HERE TO
CHANGE
THE WAY
INDIA
PLAYS WITH
TWO WHEELS
CHECK IT OUT AT
HALL NO.6
THE
AU
MOTOR
EXPO
SHOW

'''

string = string.lower()

# t = TextBlob(string)
# print t.noun_phrases

import nltk

lines = string
# function to test if something is a noun
is_noun = lambda pos: pos[:2] == 'NN'
# do the nlp stuff
tokenized = nltk.word_tokenize(lines)
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

print nouns