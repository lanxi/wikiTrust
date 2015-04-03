import os
import time

for line in open('/Users/lanxi/Desktop/Lanxi.txt'):
	url = 'http://' + line.strip()
	try:
		os.system('pagerank ' + url)
	except: 
		print 'NOT_FOUND\n'
	time.sleep(5)
