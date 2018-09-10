import re
import urllib.request
import urllib.parse
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
