import csv

output = []
with open("/Users/lanxihuang/Downloads/computer_science_pagelinks", "rb") as f:
	reader = csv.reader(f, delimiter="\t")
	count = 1
	receiver = "somenum"
	for row in reader:
		if str(row[1]) == receiver:
			count += 1
		else:
			if receiver != "somenum":
				writeline = [receiver,str(count)]
				output.append(writeline)
				receiver = row[1]
				count = 1

with open("/Users/lanxihuang/Downloads/linkcounts.csv", "wb") as f2:
	writer = csv.writer(f2)
	for row in output:
		writer.writerow(row)
