import csv 


f = open("brown.csv", "r")
reader = csv.reader(f, delimiter=',')

corpus = [[],[]]

for row in reader:
    for i in range(2):
        corpus[i].append(row[i])


size = len(corpus[1])

#grab tags
tags = {}

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
for i in range(size):
    corpus[1][i] = corpus[1][i].split()
    corpus[0][i] = corpus[0][i].split()
    current = corpus[1][i]
    current_size = len(current)
    for c in range (current_size):
        if current[c] not in tags:
            d = data()
            tags[current[c]] = d 
            tags[current[c]].count += 1
        else:
            tags[current[c]].count += 1

#grab transitions for tags
for i in range(size):
    current = corpus[1][i]
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
for i in range(size):
    current = corpus[0][i]
    current_size = len(current)
    for c in range (current_size):
        if current[c] not in lexicon:
            d = data()
            lexicon[current[c]] = d 
            lexicon[current[c]].count += 1
        else:
            lexicon[current[c]].count += 1

#grab transitions for lexicon
for i in range(size):
    sent = corpus[0][i]
    tsent = corpus[1][i]
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

#best transition
def bpath(transition):
    item = [None, None]
    for key in transition:
        if item[0] == None: 
            item[0] = key 
            item[1] = transition[key].probability
        else:
            if item[1] < transition[key].probability:
                item[0] = key 
                item[1] = transition[key].probability  

    return item[0], item[1]


#limited word

print(bpath(lexicon["ostracism"].transitions))