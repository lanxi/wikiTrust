from lxml import html
import requests

baseURL = 'https://scholar.google.com'
# the DOI/ISBN for this reference
# parse the reference number
relativeURL = '/scholar?q='+'################'
reference_page = requests.get(baseURL+relativeURL)
tree = html.fromstring(reference_page)

title = tree.xpath('//div[@id="gs_ccl"]/div[1]//h3[@class="gs_rt"]/text()')
# author links
author = tree.xpath('//div[@id="gs_ccl"]/div[1]//h3[@class="gs_a"]/a/@href')
# number of citations
citation = tree.xpath('//div[@id="gs_ccl"]/div[1]//h3[@class="gs_fl"]/a[1]/text()')
citation_string = citation[0]
number = [int(s) for s in citation_string.split() if s.isdigit()]
citation_number = number[0]

# author h-index
for author_URL in author:
	author_page = requests.get(baseURL+authorURL)
	tree = html.fromstring(author_page)
	h = tree.xpath('//table[@id="gsc_rsb_st"]//tr[3]/td[@class="gsc_rsb_std"]/text()')
	h_all = h[0]
	h_2010 = h[1]
