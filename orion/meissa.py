import log
import urllib.request
import http.cookiejar

class Meissa():
    timeout = 100
    max_page = 1

    __tags = ["热门","最新","经典","可播放","豆瓣高分","冷门佳片","华语","欧美","韩国","日本","动作","喜剧","爱情","科幻","悬疑","恐怖","文艺"]

    __urls = {
        "search": "http://movie.douban.com/j/search_subjects"
    }

    def __init__(self):
        self.init_opener()

    def init_opener(self, head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }):
        self.head = head
        cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        self.opener.addheaders = header
        return self.opener

    def get_movices(self, tag, data = {
        'type': 'movie',
        'sort': 'recommend',
        'page_limit': 20,
        }):

        data['tag'] = tag
        for x in range(0, self.max_page):
            data['page_start'] = x
            params = urllib.parse.urlencode(data)
            res = self.opener.open(self.__urls["search"], params, timeout = self.timeout)
            result = res.read()
            print(result.decode())


def main():
    m = Meissa()
    m.get_movices("冷门佳片")

if __name__ == '__main__':
    main()