import csv
import re
from reference import ref_quality
from tor_setup import tor_setup

tor_setup()
file = open('/Users/lanxihuang/Desktop/computer_science_citations.csv','rU')
csv_file = csv.reader(file)
output = open("reference.txt","wb")

for row in csv_file:
	if row[0].isdigit():
		# new page ID
		output.write(row[0] + ', ')
		ref_points = 0
	elif ((row[0] == 'journal') or (row[0] == 'book')):
		# new ref
		ref_name = row[1]
		ref_name_parsed = re.sub('','',ref_name)
		ref_name_parsed = re.sub('[\s]+','%20',ref_name_parsed)
		#print ref_name_parsed
		ref_points += ref_quality(ref_name_parsed)
		#print ref_points
	else:
		# end of previous page
		output.write(str(ref_points) + '\n')
output.close()
