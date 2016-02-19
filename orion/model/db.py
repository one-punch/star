from peewee import *
import datetime

database = MySQLDatabase("onepunch", host="127.0.0.1", port=3306, user="root", passwd="qazwsx")
prefix = "douban_"


class BaseModel(Model):
	class Meta:
		database = database

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



class Movie(BaseModel):
	id = PrimaryKeyField()
	douban_id = IntegerField(unique=True)
	title = CharField()
	douban_url = CharField()
	rate = FloatField()
	year = IntegerField()
	douban_mobile_url = CharField()
	ratings_count = IntegerField()
	summary = TextField()
	original_title = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = prefix + "movies"