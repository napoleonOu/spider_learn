import re
import urllib.request
import urllib.parse
import lxml.html
import csv
#learn from https://zhuanlan.zhihu.com/p/28621516
#1、下载网站源码
def download(url,user_agent='wswp',proxy=None,num_retries=2,timout=5):
    print('Begin Download:',url)

    #代理
    headers={'User-agent':user_agent}
    request=urllib.request.Request(url,headers=headers)

    #配置
    opener=urllib.request.build_opener()

    #是否代理
    if proxy:
        proxy_parms={urllib.parse.urlparse(url).scheme:proxy} #scheme 找不到
        opener.add_handler(urllib.request.ProxyHandler(proxy_parms))
    try:
        html=opener.open(request,timeout=timout).read() #html 用配置打开请求 并读取
    except urllib.request.URLError as e:
        print('Download error as:',e.reason)
        html=None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code <600: #e.code 找不到
                html=download(url,user_agent,num_retries-1)
    except Exception as e:
        print('Exception as:',e)
        html=None
    return html
#2、获取网页中的链接地址
def get_links(html):
    if html:
        page_regex=re.compile('<a[^>+href=["\']',re.IGNORECASE)
        return page_regex.findall(html.decode)
    else:
        return ""

#编写爬取规则，解析获得数据
def scrape_callback(url,html):
    csslist =['span[property="v:itemreviewed"]','span.year','strong[property="v:average"]']
    try:
        tree=lxml.html.fromstring(html)
        row=[tree.cssselect('{0}'.format(field))[0].text for field in csslist] # dont know
        print(url,row)
    except Exception as e:
        print("Callback error as:",e)

#爬虫入口
def link_crawler(seed_url,link_regex,max_depth=2,scrape_callback=None):
    crawler_queue=[seed_url] #爬取首页地址中特定链接，保存在队列中
    seens={seed_url:1} #map 存取爬取深度

    while crawler_queue:
        url=crawler_queue.pop()
        html=download(url)
        depth=seens[url]
        print("深度："depth)

        for link in get_links(html):
            if depth != max_depth and re.search(link_regex,link):
                link=urllib.parse.urljoin(seed_url,link) #拼接 标准网页链接

                if link not in seens:
                    seens[link]=depth+1
                    crawler_queue.append(link)

        #有回调函数
        if scrape_callback:
            scrape_callback(url,html)

class ScrapeCallback:
    def __init__(self):