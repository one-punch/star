import log
import urllib.request
import http.cookiejar
import json
from subject import *
import model.db as model
from time import sleep
from alnilam import Alnilam
import config
import  threading


options = config.options
logger = log.logger()

__tags = ["热门","最新","经典","可播放","豆瓣高分","冷门佳片","华语","欧美","韩国","日本","动作","喜剧","爱情","科幻","悬疑","恐怖","文艺"]


class Subject():
    def __init__(self, d):
        self.__dict__ = d

class Meissa():
    timeout = 100
    page_limit = 20


    __urls = {
        "search": "http://movie.douban.com/j/search_subjects",
        "detail": "http://api.douban.com/v2/movie/subject/%s"
    }

    def __init__(self):
        self.x = 0
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

    def get_movies(self, start_num, tag, data = {
        'type': 'movie',
        'sort': 'recommend',
        'page_limit': page_limit,
        }):

        data['tag'] = tag
        for x in range(start_num, options.max_page):
            self.x = x
            data['page_start'] = x * self.page_limit
            params = urllib.parse.urlencode(data)
            res = self.opener.open(self.__urls["search"] + "?" + params, timeout = self.timeout)
            result = res.read()
            subjects_json = json.loads(result.decode())
            self.push_to_queue(subjects_json["subjects"])
            sleep(1)

    def get_detail(self, subject_id):
        url = self.__urls["detail"] % (subject_id+"")
        res = self.opener.open(url, timeout = self.timeout)
        result = json.loads((res.read().decode()))
        return Subject(result)

    def push_to_queue(self, movies):
        for movie_json in movies:
            movie = model.MovieQueue.select().where(model.MovieQueue.douban_id == movie_json["id"]).limit(1).first()
            if movie is None:
                model.MovieQueue.create(douban_id=movie_json["id"])


def get_continue():
    config = model.Config.select().where(model.Config.name == "continue").limit(1).first()
    if config is not None:
        return Subject(json.loads(config.value))
    else:
        return Subject({ "start_num": 0, "tag_index": 0 })

def save_state(start_num, tag_index):
    config = model.Config.select().where(model.Config.name == "continue").limit(1).first()
    if config is None:
        model.Config.create(name="continue", value=json.dumps({ "start_num": start_num, "tag_index": tag_index }))
    else:
        config.value = json.dumps({ "start_num": start_num, "tag_index": tag_index })
        config.save()

def get_movie_detail():
    meissa = Meissa()
    alnilam = Alnilam()

    while True:
        available = model.MovieQueue.select().where(model.MovieQueue.state == 0).count()
        if available > 0:
            prepare_movies =  model.MovieQueue.select().where(model.MovieQueue.state == 0).limit(100)
            for m in prepare_movies:
                detail = meissa.get_detail(m.douban_id)
                with model.database.atomic() as txn:
                    try:
                        alnilam.generate_movie(detail)
                        m.state = 1
                        m.save()
                        logger.info(detail.id + " " + detail.title)
                    except Exception as e:
                        logger.error(e)
                        txn.rollback()
                sleep(2)
        else:
            sleep(2)


def movie_detail_start():
    sleep(2)
    threading.Thread(target=get_movie_detail, name="get_movie_detail").start()

def main():
    first = get_continue()
    meissa = Meissa()
    start_num = first.start_num

    movie_detail_start()
    for idx, tag in enumerate(__tags):
        if idx < first.tag_index:
            continue
        try:
            meissa.get_movies(start_num, tag)
            start_num = 0
        except (KeyboardInterrupt, SystemExit):
            save_state(meissa.x if meissa.x >= 0 else 0, idx)
            raise

    while True:
        available = model.MovieQueue.select().where(model.MovieQueue.state == 0).count()
        if available == 0:
            logger.info("finish")
            break


if __name__ == '__main__':
    main()