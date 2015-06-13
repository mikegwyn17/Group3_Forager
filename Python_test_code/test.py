import requests
from bs4 import BeautifulSoup
import tldextract
url = "http://spsu.edu"
domain = str(tldextract.extract(url).domain)
requests.packages.urllib3.disable_warnings()
current_domain = str(tldextract.extract(url).domain)
if current_domain not in domain:
    print ("work")
print(domain)
to_search = []
r = requests.get(url, allow_redirects = True, verify = False)
print(r.status_code)
source_code = r.text
soup = BeautifulSoup(source_code)
for css in soup.findAll('link'):
    href = css.get('href')
    if href[0:4] == 'http' or href[0:5] == 'https':
        href = href
    else:
        href = url + href
    print(href)
    to_search.append(href)

for image in to_search:
    r = requests.head(image)
    print(r.status_code)


