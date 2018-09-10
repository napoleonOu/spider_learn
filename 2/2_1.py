import re
import urllib.response
import urllib.request
def download(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content

url='http://example.webscraping.com/places/default/view/Aland-Islands-2'
html=download(url)
print(re.findall('<td class="w2p_fw">(.*?)</td>',html)[1])


