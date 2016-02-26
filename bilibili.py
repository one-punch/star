import urllib.request
import http.cookiejar
import hashlib
import json

def GetString(t):
    if type(t) == int:
        return str(t)
    return t

def GetSign(params, appkey, AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
    """
    params['appkey']=appkey
    data = ""
    paras = sorted(params.keys())
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + str(urllib.parse.quote(GetString(params[para])))
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update( (data+AppSecret).encode('utf-8') )
    return data+'&sign='+m.hexdigest()

def get_opener():
    head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

def get_info(opener, id, page):
    url = "http://api.bilibili.cn/view"
    appkey = "85eb6835b0a1034e"
    AppSecret = "2ad42749773c441109bdc0191257a664"
    params = {'id': id,'page': page}
    sign = GetSign(params, appkey, AppSecret)
    res = opener.open(url + "?" + sign).read()
    print(url + "?" + sign)
    print( json.loads(res.decode()) )



if __name__ == "__main__":
    url = "http://api.bilibili.cn/search"
    appkey = "85eb6835b0a1034e"
    AppSecret = "2ad42749773c441109bdc0191257a664"

    opener = get_opener()

    params = {}

    params['keyword'] = GetString("丹麦女孩")
    params['order'] = GetString("default")
    params['pagesize'] = GetString("20")
    params['page'] = GetString("2")

    sign = GetSign(params, appkey, AppSecret)
    print(sign)
    res = opener.open(url + "?" + sign).read()
    print( json.loads(res.decode()) )
    print(url + "?" + sign)

    # get_info(opener, 2035719, 1)

