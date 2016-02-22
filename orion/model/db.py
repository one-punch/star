from peewee import *
import datetime

database = MySQLDatabase("onepunch", host="127.0.0.1", port=3306, user="root", passwd="qazwsx")
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
		MovieCast
	]

	database.connect()
	database.create_tables(__all__)