import wfreq
import csv 

f = open("brown.csv", "r")
reader = csv.reader(f, delimiter=',')

corpus = [[],[]]

for row in reader:
    for i in range(2):
        corpus[i].append(row[i])

size = len(corpus[1])
train_size = int(size * 0.75)
train_corpus = [[],[]]
test_corpus = [[],[]]

for r in range(train_size):
    train_corpus[0].append(corpus[0][r].split())
    train_corpus[1].append(corpus[1][r].split())

for r in range(train_size, size, 1):
    test_corpus[0].append(corpus[0][r].split())
    test_corpus[1].append(corpus[1][r].split())

test_size = len(test_corpus[0])

#grab tags
tags = {}

#metadata for transitions
class pdata():
    def __init__(self):
        self.count = 0
        self.probability = 0.0

    def update(self, count):
        self.probability = self.count / count

class data():
    def __init__(self):
        self.count = 0
        self.transitions = {}

#add unique tags into the dictionary tag 
#split the untag section and tagged section 
for i in range(train_size):
    current = train_corpus[1][i]
    current_size = len(current)
    for c in range (current_size):
        if current[c] not in tags:
            d = data()
            tags[current[c]] = d 
            tags[current[c]].count += 1
        else:
            tags[current[c]].count += 1

#grab transitions for tags
for i in range(train_size):
    current = train_corpus[1][i]
    current_size = len(current)
    for c in range (current_size):
        if c != current_size - 1:
            if current[c + 1] not in tags[current[c]].transitions:
                item = pdata()
                tags[current[c]].transitions[current[c + 1]] = item
                tags[current[c]].transitions[current[c + 1]].count += 1
                tags[current[c]].transitions[current[c + 1]].update(tags[current[c]].count)
            else:
                tags[current[c]].transitions[current[c + 1]].count += 1
                tags[current[c]].transitions[current[c + 1]].update(tags[current[c]].count)

#fill in lexicon
lexicon = {}

for i in range(train_size):
    sentence = train_corpus[0][i]
    sentence_size = len(sentence)
    for c in range (sentence_size):
        if sentence[c] not in lexicon:
            w = data()
            lexicon[sentence[c]] = w 
            lexicon[sentence[c]].count += 1
        else:
            lexicon[sentence[c]].count += 1

#grab transitions for lexicon
for i in range(train_size):
    sent = train_corpus[0][i]
    tsent = train_corpus[1][i]
    current_size = len(sent)
    for c in range (current_size):
        if c != current_size - 1:
            if tsent[c] not in lexicon[sent[c]].transitions:
                item = pdata()
                lexicon[sent[c]].transitions[tsent[c]] = item
                lexicon[sent[c]].transitions[tsent[c]].count += 1
                lexicon[sent[c]].transitions[tsent[c]].update(lexicon[sent[c]].count)
            else:
                lexicon[sent[c]].transitions[tsent[c]].count += 1
                lexicon[sent[c]].transitions[tsent[c]].update(lexicon[sent[c]].count)

#grab transitions with probability of 1
def axioms():
    t = {}
    for token in tags:
        if len(tags[token].transitions) == 1:
            t[token] = tags[token]
    
    return t

#best transition
def bpath(transition):
    item = ["UKWN", 0.0]
    for key in transition:
        if item[0] == None: 
            item[0] = key 
            item[1] = transition[key].probability
            print("HELLO",item[1])
        else:
            if item[1] < transition[key].probability:
                item[0] = key 
                item[1] = transition[key].probability  

    return item[0], item[1]

#grab the frequent words and filled in frequent lexicons
freqW = wfreq.most_freq_words
freqLex = {}

for w in freqW:
    if w in lexicon:
        freqLex[w] = lexicon[w]
    if w.capitalize() in lexicon:
        freqLex[w.capitalize()] = lexicon[w.capitalize()]

axiom = axioms()

def tokenize(sentence):
    tagged_sentence = []
    tags_prob = []
    for word in sentence:
        if word != ".":        
            if word in freqLex:
                item = bpath(freqLex[word].transitions)
                tagged_sentence.append(item[0])
                tags_prob.append(item[1])

            #look at transitions here
            elif len(tagged_sentence) > 0:
                if tagged_sentence[-1] in axiom:
                    item = bpath(axiom[tagged_sentence[-1]].transitions)
                    tagged_sentence.append(item[0])
                    tags_prob.append(item[1])

                elif tagged_sentence[-1] in tags:
                    item = bpath(tags[tagged_sentence[-1]].transitions)
                    tagged_sentence.append(item[0])
                    tags_prob.append(item[1])
                
                else:
                    tagged_sentence.append("UKWN")
                    tags_prob.append("0.0")

        elif word == ".":
            tagged_sentence.append(".")
            tags_prob.append(1.0)

        elif word == ",":
            tagged_sentence.append(",")
            tags_prob.append(1.0)
        
        else:
            tagged_sentence.append("UKWN")
            tags_prob.append("0.0")

    return tagged_sentence, tags_prob


test_result = [[],[]]

for r in range(test_size):
    test_result[0].append(tokenize(test_corpus[0][r]))
    test_result[1].append(test_corpus[1][r])

accuracies = []
test_result_size = len(test_result[0])

for r in range(test_result_size):
    current_size = len(test_result[0][r][0])
    acc = 0.0
    if current_size != 0:    
        for c in range(current_size):
            if test_result[0][r][0][c] == test_result[1][r][c]:
                acc += 1.0
        
        acc = acc / current_size
        accuracies.append(acc)

print(sum(accuracies) / len(accuracies))
