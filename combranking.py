import csv

linkcounts = open("/Users/lanxihuang/Downloads/linkcounts.csv", "rb")
refs = open("/Users/lanxihuang/Desktop/refs.txt", "rb")

reader1 = csv.reader(refs)
reader2 = csv.reader(linkcounts, delimiter=",")

dictionary = {}
output = []
for line in reader2:
	pageid = line[0]
	links = line[1]
	dictionary[pageid] = links

for row in reader1:
	if dictionary.has_key(row[0]):
		pageid = row[0]
		writeline = [pageid, dictionary[pageid], row[1]]
		output.append(writeline)

with open("/Users/lanxihuang/Downloads/combranking.csv", "wb") as f2:
	writer = csv.writer(f2)
	for row in output:
		writer.writerow(row)
