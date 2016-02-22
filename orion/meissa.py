import log
import urllib.request
import http.cookiejar
import json
from subject import *
import model.db as model
from time import sleep
from alnilam import Alnilam

class Subject():
    def __init__(self, d):
        self.__dict__ = d

class Meissa():
    timeout = 100
    max_page = 2
    page_limit = 20

    __tags = ["热门","最新","经典","可播放","豆瓣高分","冷门佳片","华语","欧美","韩国","日本","动作","喜剧","爱情","科幻","悬疑","恐怖","文艺"]

    __urls = {
        "search": "http://movie.douban.com/j/search_subjects",
        "detail": "http://api.douban.com/v2/movie/subject/%s"
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

    def get_movies(self, tag, data = {
        'type': 'movie',
        'sort': 'recommend',
        'page_limit': page_limit,
        }):

        subjects = []
        data['tag'] = tag
        for x in range(0, self.max_page):
            data['page_start'] = x * self.page_limit
            params = urllib.parse.urlencode(data)
            res = self.opener.open(self.__urls["search"] + "?" + params, timeout = self.timeout)
            result = res.read()
            subjects_json = json.loads(result.decode())
            subjects += self.load_subjects(subjects_json["subjects"])

        print(len(subjects))
        return subjects

    def load_subjects(self, subjects_json):
        subjects  = []
        for x in subjects_json:
            subjects.append(Subject(x))
        return subjects

    def get_detail(self, subject_id):
        url = self.__urls["detail"] % (subject_id+"")
        res = self.opener.open(url, timeout = self.timeout)
        result = json.loads((res.read().decode()))
        return Subject(result)


def function():
    pass


def main():
    # model.init_db()
    meissa = Meissa()
    movies = meissa.get_movies("冷门佳片")
    alnilam = Alnilam()
    index = 1

    for movie_json in movies:
        detail = meissa.get_detail(movie_json.id)
        alnilam.generate_movie(movie_json, detail)
        sleep(2)
        print(str(index))
        index+=1


if __name__ == '__main__':
    main()