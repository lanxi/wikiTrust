import time
import random
import requests
import ssl
from functools import wraps
import cookielib as cookiejar
from bs4 import BeautifulSoup

class BlockAll(cookiejar.CookiePolicy):
  return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
  netscape = True
  rfc2965 = hide_cookie2 = False

def LoadUserAgents(uafile="/Users/lanxihuang/Desktop/user_agents.txt"):
  uas = []
  with open(uafile, 'rb') as uaf:
    for ua in uaf.readlines():
      if ua:
        uas.append(ua.strip()[1:-1-1])
  random.shuffle(uas)
  return uas

def sslwrap(func):
  @wraps(func)
  def bar(*args, **kw):
    kw['ssl_version'] = ssl.PROTOCOL_TLSv1
    return func(*args, **kw)
  return bar

def ref_quality(refID):
  quality = 0
  baseURL = 'https://scholar.google.com'
  # the DOI/ISBN for this reference
  # parse the reference number
  relativeURL = '/scholar?q='+ refID
  print relativeURL
  uas = LoadUserAgents()

  s = requests.Session()
  s.cookies.set_policy(BlockAll())
  ssl.wrap_socket = sslwrap(ssl.wrap_socket)
  ua = random.choice(uas)
  headers = {"User-Agent": ua}
  
  reference_page = s.get(baseURL+relativeURL, verify=False, headers=headers)
  time.sleep(5)
  soup = BeautifulSoup(reference_page.text)

  # title
  #title = soup.find("h3", {"class": "gs_rt"}).text
  # author links
  authors = soup.find("div", {"class": "gs_a"})
  if bool(authors) == True:
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
      num = [int(char) for char in citation.split() if char.isdigit()]
      if bool(num) == True:
        citation_num = num[0]
        print ('citation: ' + str(citation_num))
        quality += citation_num
    else:
      print ('no number of citation found')
   
    # author h-index
    if bool(author_ref) == True:
      for a in author_ref:
        ua = random.choice(uas)
        headers = {"User-Agent": ua}
        author_page = s.get(baseURL+a, verify=False, headers=headers)
        time.sleep(5)
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
        print ('h-index: ' + str(h_index))
        quality += h_index
      else:
        print ('no h-index found')
    else:
      print ('no author reference link found')

  try:
    s.close()
  except AttributeError:
    print ('session close method failed')
  s = None
  return quality
