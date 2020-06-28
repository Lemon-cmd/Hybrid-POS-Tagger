import csv 

f = open("unigram_freq.csv", "r")
reader = csv.reader(f, delimiter=',')

frequency = {}
mean = 0.0
for row in reader:
    frequency[row[0]] = float(row[1])
    mean += frequency[row[0]]

mean /= len(frequency)

stdeviation = 0.0

for word in frequency:
    stdeviation += ((frequency[word] - mean)**2)

stdeviation /= len(frequency)
stdeviation = stdeviation**0.5

most_freq_words = {}

for word in frequency:
    d = (frequency[word] - mean) / stdeviation
    if not(d > -2 and d < 2):
        most_freq_words[word] = frequency[word]

