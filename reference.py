import requests
from bs4 import BeautifulSoup

def ref_quality(refID):
 quality = 0
 baseURL = 'https://scholar.google.com'
 # the DOI/ISBN for this reference
 # parse the reference number
 relativeURL = '/scholar?q='+ refID
 reference_page = requests.get(baseURL+relativeURL, verify=False)
 soup = BeautifulSoup(reference_page.text)
 
 # title
 title = soup.find("h3", {"class": "gs_rt"}).text
 # author links
 authors = test=soup.find("div", {"class": "gs_a"})
 author_ref = []
 for a in authors.find_all('a', href=True):
  author_ref.append(a['href'])
 
 # number of citations
 gs_fl = soup.find_all("div", {"class": "gs_fl"})
 citation = None
 for c in gs_fl:
  if c['class'] == ['gs_fl']:
   citation = c.find('a', href=True).text
   break
 
 if bool(citation) == True:
  citation_num = [int(s) for s in citation.split() if s.isdigit()][0]
  quality += citation_num
 else:
  print ('no number of citation found')
 
 # author h-index
 user_agent = {'User-agent': 'Mozilla/5.0'}
 if bool(author_ref) == True:
  for a in author_ref:
   author_page = requests.get(baseURL+a, verify=False, headers=user_agent)
   #print (author_page)
   soup = BeautifulSoup(author_page.text)
   index = soup.find_all("td",{"class": "gsc_rsb_std"})
   indexes = []
   for i in index:
    indexes.append(i.text)
   h_index = None
   h_index_2010 = None
   if bool(indexes) == True:
    h_index = int(indexes[2].encode("ascii"))
    h_index_2010 = int(indexes[3].encode("ascii"))
    quality += h_index
   else:
    print ('no h-index found')
 else:
  print ('no author reference link found')
 
 return quality
