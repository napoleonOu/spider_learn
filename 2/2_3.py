import lxml.html
import urllib.response
import urllib.request
from lxml import etree
import lxml.cssselect
def download(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content
def scrape(url):
    #tree=lxml.html.fromstring(html)
    #tree=lxml.html.parse(url).getroot()
    #print("tree:")
    #print(tree)
    html = etree.HTML(url)
    result = etree.tostring(html)
    #print(result)
    #print(html)
    #td=tree.ccssselect('tr#places_area__row')[0]
    #print(td)
    #return td.get_text()
    return result
#https://stackoverflow.com/questions/19730476/lxml-etree-elementtree-object-has-no-attribute-cssselect
#import lxml.html
#broken_html='<ul class=country><li>Area<li>Population</ul>'

#tree=lxml.html.fromstring(broken_html)
#print(tree)
#fixed_html=lxml.html.tostring(tree,pretty_print=True)
#print(fixed_html)
if __name__ == '__main__':
    #url='http://example.webscraping.com/places/default/view/Aland-Islands-2'
    #html=download(url)
    html='<ul class=country><li>Area<li>Population</ul>'
    print(scrape(html))