import os
import time

for line in open('/Users/lanxihuang/Desktop/Anusha.txt'):
	url = 'http://' + line.strip()
	try:
		os.system('pagerank ' + url)
	except: 
		print 'NOT_FOUND\n'
	time.sleep(5)
