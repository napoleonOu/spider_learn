import urllib.request
import urllib.response
from bs4 import BeautifulSoup
def download(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content
def scrape(html):
    soup=BeautifulSoup(html)
    tr=soup.find(attrs={'id':'places_area__row'})
    print("tr:")
    print(tr)
    td=tr.find(attrs={'class':'w2p_fw'})
    print("td:")
    #print(td)
    return td.get_text()

#broken_html='<ul class=country><li>Area<li>Population</ul>'
#soup=BeautifulSoup(broken_html,'html.parser')
#fixed_html=soup.prettify()
#print(fixed_html)
if __name__ == '__main__':
    url='http://example.webscraping.com/places/default/view/Aland-Islands-2'
    html=download(url)
    print(scrape(html))