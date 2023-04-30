from keytotext import pipeline
import csv
nlp = pipeline("k2t-base")
config = {"do_sample": True, "num_beams": 4, "no_repeat_ngram_size": 3, "early_stopping": True}
li=[]
with open('dataForSearch.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        li.append(row)
new_li=[]
for i in range(len(li)-50):
    new_li.append(nlp([li[i:i+50]], **config))
print(new_li)