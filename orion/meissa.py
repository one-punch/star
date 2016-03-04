import log
import urllib.request
import http.cookiejar
import json
from subject import *
import model.db as model
from time import sleep
from alnilam import Alnilam
from betelgeuse import Betelgeuse
from bellatrix import Planet
from bellatrix import Bellatrix
import config
import  threading
import sys


options = config.options

__tags = ["热门","最新","经典","可播放", "豆瓣高分","冷门佳片","华语","欧美","韩国","日本","动作","喜剧","爱情","科幻","悬疑","恐怖","文艺"]


class Subject():
    def __init__(self, d):
        self.__dict__ = d

class Meissa(Planet):
    timeout = 100

    __urls = {
        "search": "http://movie.douban.com/j/search_subjects",
        "detail": "http://api.douban.com/v2/movie/subject/%s"
    }

    def __init__(self):
        self.x = 0
        self.init_opener()

    def get_movies(self, start_num, tag, data = {
        'type': 'movie',
        'sort': 'recommend',
        'page_limit': options.page_limit,
        }):

        data['tag'] = tag
        for x in range(start_num, options.max_page):
            self.x = x
            data['page_start'] = x * options.page_limit
            params = urllib.parse.urlencode(data)
            log.logger().info("get: " + self.__urls["search"] + "?" + params)
            res = self.opener.open(self.__urls["search"] + "?" + params, timeout = self.timeout)
            result = res.read()
            subjects_json = json.loads(result.decode())
            self.push_to_queue(subjects_json["subjects"])
            sleep(1)

    def get_detail(self, subject_id):
        url = self.__urls["detail"] % (subject_id+"")
        log.logger().info("get: " + url)
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
                        log.logger().info(detail.id + " " + detail.title)
                    except Exception as e:
                        log.logger().error(e)
                        txn.rollback()
                sleep(2)
        else:
            sleep(2)


def movie_detail_start():
    sleep(2)
    thread = threading.Thread(target=get_movie_detail, name="get_movie_detail")
    thread.setDaemon(True)
    thread.start()

def allow_type(typename):
    __types__ = ['电影']
    for _type in __types__:
        if typename.endswith(_type):
            return True
    return False

def get_movie_url_from_bilibili():
    betelgeuse = Betelgeuse()
    bellatrix = Bellatrix(options.appkey, options.appsecret)

    while True:
        available = model.MovieQueue.select().where(model.MovieQueue.state == 1).count()
        if available > 0:
            prepare_movies =  model.MovieQueue.select().where(model.MovieQueue.state == 1).limit(100)
            for m in prepare_movies:
                movie = Alnilam.get_first_movie(m.douban_id)
                try:
                    search_reault = bellatrix.search(movie.title)
                    if search_reault.is_done:
                        match_movie = False
                        for sr in search_reault.result:
                            if allow_type(sr["typename"]):
                                match_movie = True
                                detail = bellatrix.view(sr["aid"])
                                pages = detail.pages
                                for page in range(1, pages+1):
                                    if hasattr(detail, 'cid'):
                                        detail.download, detail.expires = bellatrix.build_download_url(detail.cid)
                                    with model.database.atomic() as txn:
                                        try:
                                            betelgeuse.build_bilibili(sr, m.douban_id)
                                            betelgeuse.replenish_bilibili(sr["aid"], detail)
                                            m.state = 2
                                            m.save()
                                        except Exception as e:
                                            log.logger().error(e)
                                            txn.rollback()
                                    detail = bellatrix.view(sr["aid"], page + 1)
                                    sleep(2)
                                sleep(2)
                        if not match_movie:
                            m.state = 3
                            m.save()
                    sleep(1)
                except Exception as e:
                    log.logger().error(e)
        else:
            sleep(2)


def bilibili_media_start():
    sleep(2)
    thread = threading.Thread(target=get_movie_url_from_bilibili, name="get_movie_url_from_bilibili")
    thread.setDaemon(True)
    thread.start()

def main():
    first = get_continue()
    meissa = Meissa()
    start_num = first.start_num

    movie_detail_start()
    bilibili_media_start()
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
        available = model.MovieQueue.select().where( (model.MovieQueue.state == 0) | (model.MovieQueue.state == 1) ).count()
        if available == 0:
            log.logger().info("douban finish")
            sys.exit(3)
        else:
            sleep(1200)

if __name__ == '__main__':
    main()