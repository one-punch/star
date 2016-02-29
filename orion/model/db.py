from peewee import *
import datetime
import config

options = config.options

database = MySQLDatabase(options.database, host=options.host, port=options.port, user=options.user, passwd=options.password)
prefix = "douban_"

class BaseModel(Model):
	class Meta:
		database = database

	def __class_name__(self):
		return self.__class__.__name__

class ImageManager(object):

	def cover(self):
		img = Image.select().where( Image.item_type == self.__class__.__name__, Image.item_id == self.id).first()
		if img is not None:
			return img
		else:
			return ""


class Image(BaseModel):
	id = PrimaryKeyField()
	small = CharField()
	medium = CharField()
	large = CharField()
	item_type = CharField()
	item_id = IntegerField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "images"


class Country(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	code = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "countries"


class Genre(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	code = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "genres"


class Celebrity(BaseModel, ImageManager):
	id = PrimaryKeyField()
	douban_id = IntegerField(unique=True)
	name = CharField()
	douban_url = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "celebrities"


class Movie(BaseModel, ImageManager):
	id = PrimaryKeyField()
	douban_id = IntegerField(unique=True)
	title = CharField()
	douban_url = CharField()
	rate = FloatField()
	year = IntegerField()
	douban_mobile_url = CharField()
	ratings_count = IntegerField()
	collect_count = IntegerField()
	reviews_count = IntegerField()
	summary = TextField()
	original_title = CharField()
	url = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies"

	def countries(self):
		return 	(Country.select()
				.join(MovieCountry)
				.join(Movie))

	def genres(self):
		return 	(Genre.select()
				.join(MovieGenre)
				.join(Movie))

	def directors(self):
		return 	(Celebrity.select()
				.join(MovieDirector)
				.join(Movie))

	def casts(self):
		return 	(Celebrity.select()
				.join(MovieCast)
				.join(Movie))


class MovieCountry(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	country = ForeignKeyField(Country)
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_countries"

class MovieGenre(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	genre = ForeignKeyField(Genre)
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_genres"


class MovieDirector(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	director = ForeignKeyField(Celebrity)
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_directors"

class MovieCast(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	cast = ForeignKeyField(Celebrity)
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_casts"

class Config(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	value = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "configs"

class MovieQueue(BaseModel):
	id = PrimaryKeyField()
	douban_id = CharField()
	state = IntegerField(default=0)
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movie_queue"


class BilibiliMovie(BaseModel):
	id = PrimaryKeyField()
	douban_id = IntegerField()
	avid = IntegerField()
	author = CharField()
	typename = CharField()
	arcurl = CharField()


"type": "video",
            "id": 3658407,
            "author": "无敌赵大宝941",
            "mid": 21787261,
            "typename": "电影相关",
            "arcurl": "http://www.bilibili.com/video/av3658407/",
            "aid": "3658407",
            "description": "自制 无论他是韦格纳还是莉莉，格尔达都爱他，他是她的缪斯也是她的爱人\r\n这个电影很让人感动也让人揪心，是一部非常棒的电影",
            "title": "丹麦女孩",
            "arcrank": "0",
            "pic": "http://i0.hdslb.com/video/a2/a27341c8157ed529408165016f3de81b.jpg",
            "play": 32772,
            "video_review": 34,
            "favorites": 593,
            "tag": "电影剪辑,丹麦女孩",
            "review": 12,
            "pubdate": 1453656091

	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "bilibili_movies"



def init_db():
	__all__ = [
		Image,
		Country,
		Genre,
		Celebrity,
		Movie,
		MovieCountry,
		MovieGenre,
		MovieDirector,
		MovieCast,
		Config,
		MovieQueue
	]

	database.connect()
	database.create_tables(__all__)

if __name__ == '__main__':
    init_db()