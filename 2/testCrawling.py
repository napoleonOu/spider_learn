import re
import urllib.request
import urllib.parse
import lxml.html
import csv


def dowmload(url, user_agent='wswp', proxy=None, num_retries=2, timeout=5):
    print('DownloadURL:',url)

    headers = {'User-agent':user_agent}
    request = urllib.request.Request(url, headers=headers)

    opener = urllib.request.build_opener()

    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = opener.open(request, timeout=timeout).read()
    except urllib.request.URLError as e:
        print('Download error:',e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code <600:
                html = dowmload(url, user_agent, num_retries-1)
    except Exception as e:
        print('error :',e)
        html = None

    return html


def get_links(html):
    if html:
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        return  webpage_regex.findall(html.decode('utf-8'))
    else:
        return ""


def scrape_callback(url,html):
    csslist = ['span[property = "v:itemreviewed"]', 'span.year', 'strong[property="v:average"]']
    try:
        tree = lxml.html.fromstring(html)
        row = [tree.cssselect('{0}'.format(field))[0].text for field in csslist]
        print(url, row)
    except Exception as e:
        print("ScrapeCallback error:",e)


def link_crawler(seed_url, link_regex, max_depath=2, scrape_callback=None):
    crawl_queue = [seed_url]
    seens = {seed_url:1}
    while crawl_queue:
        url = crawl_queue.pop()
        html = dowmload(url)
        depth = seens[url]
        print(depth)

        for link in get_links(html):
            if depth != max_depath and re.search(link_regex,link):
                link = urllib.parse.urljoin(seed_url, link)

                if link not in seens:
                    seens[link] = depth+1
                    crawl_queue.append(link)

        if scrape_callback:
            scrape_callback(url, html)


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w'))
        self.fields = ('name','year','score')
        self.writer.writerow(self.fields)

    def __call__(self, url,html):
        csslist = ['span[property = "v:itemreviewed"]', 'span.year','strong[property="v:average"]']
        try:
            tree = lxml.html.fromstring(html)
            row = [tree.cssselect('{0}'.format(field))[0].text for field in csslist]
            self.writer.writerow(row)
            print(url, row)
        except Exception as e:\
            print("ScrapeCallback error:",e)


if __name__ == '__main__':
    send_url = "https://movie.douban.com/"

    link_regex = '(/subject/[\d]+/)'
    link_crawler(send_url,link_regex,max_depath=2, scrape_callback=ScrapeCallback())
    #link_crawler(send_url, link_regex, max_depath=2, scrape_callback=scrape_callback)
