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
	small = CharField(null=True)
	medium = CharField(null=True)
	large = CharField(null=True)
	item_type = CharField()
	item_id = IntegerField()
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "images"


class Country(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	code = CharField(null=True)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "countries"


class Genre(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	code = CharField(null=True)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "genres"


class Celebrity(BaseModel, ImageManager):
	id = PrimaryKeyField()
	douban_id = IntegerField(unique=True)
	name = CharField(null=True)
	douban_url = CharField(null=True)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "celebrities"


class Movie(BaseModel, ImageManager):
	id = PrimaryKeyField()
	douban_id = IntegerField(unique=True)
	title = CharField()
	douban_url = CharField()
	rate = FloatField(null=True)
	year = IntegerField(null=True)
	douban_mobile_url = CharField()
	ratings_count = IntegerField()
	collect_count = IntegerField()
	reviews_count = IntegerField()
	summary = TextField()
	original_title = CharField()
	url = CharField(null=True)
	display = BooleanField(default=True)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

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
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_countries"

class MovieGenre(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	genre = ForeignKeyField(Genre)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_genres"


class MovieDirector(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	director = ForeignKeyField(Celebrity)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_directors"

class MovieCast(BaseModel):
	id = PrimaryKeyField()
	movie = ForeignKeyField(Movie)
	cast = ForeignKeyField(Celebrity)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies_casts"

class Config(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	value = CharField(null=True)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "configs"

class MovieQueue(BaseModel):
	id = PrimaryKeyField()
	douban_id = CharField()
	state = IntegerField(default=0)  # 0: 未获取详豆瓣细数据， 1：已经获取豆瓣数据未获取b站对应视频， 2： 成功获取b站对应数据， 3：未能在b站获取对应视频数据
	createdAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movie_queue"


class BilibiliMovie(BaseModel):
	id = PrimaryKeyField()
	douban_id = IntegerField()
	avid = IntegerField(unique=True)
	author = CharField()
	typename = CharField()
	arcurl = CharField(null=True)
	description = TextField()
	title = CharField()
	play = CharField(null=True)
	pages = IntegerField(default=1)
	display = BooleanField(default=True)

	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "bilibili_movies"


class BilibiliMedia(BaseModel):
	id = PrimaryKeyField()
	avid = IntegerField()
	order = IntegerField(default=1)
	mid = IntegerField()
	cid = IntegerField(unique=True)
	offsite = CharField(null=True)
	download = CharField(max_length=511)
	expires = IntegerField(default=0)
	display = BooleanField(default=True)

	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "bilibili_medias"


class BilibiliGenre(BaseModel):
	id = PrimaryKeyField()
	bilibili = ForeignKeyField(BilibiliMovie)
	genre = ForeignKeyField(Genre)
	createdAt = DateTimeField(default=datetime.datetime.now)
	updatedAt = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "bilibili_genres"

def init_bilibili():
	database.connect()
	database.create_tables([BilibiliMovie, BilibiliGenre, BilibiliMedia])

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
    init_bilibili()