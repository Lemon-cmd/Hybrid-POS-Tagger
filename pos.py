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
    for i in range (current_size):
        if current[i] not in tags:
            d = data()
            tags[current[i]] = d 
            tags[current[i]].count += 1
        else:
            tags[current[i]].count += 1

#grab transitions
for i in range(size):
    current = corpus[1][i]
    current_size = len(current)
    for i in range (current_size):
        if i != current_size - 1:
            if current[i + 1] not in tags[current[i]].transitions:
                item = pdata()
                tags[current[i]].transitions[current[i + 1]] = item
                tags[current[i]].transitions[current[i + 1]].count += 1
                tags[current[i]].transitions[current[i + 1]].update(tags[current[i]].count)
            else:
                tags[current[i]].transitions[current[i + 1]].count += 1
                tags[current[i]].transitions[current[i + 1]].update(tags[current[i]].count)

#best transition
def bpath(transitions):
    item = [None, None]
    for key in transitions:
        if item[0] == None: 
            item[0] = key 
            item[1] = transitions[key].probability
        else:
            if item[1] < transitions[key].probability:
                item[0] = key 
                item[1] = transitions[key].probability  

    return item[0], item[1]

test = ["rb"]

for i in test:
    print(bpath(tags[i].transitions))

print(corpus[0][0][1], corpus[1][0][1])