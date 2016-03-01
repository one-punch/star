import model.db as model
from alnilam import Alnilam

class Betelgeuse:

	def __init__(self):
		pass

	def get_first_bilibili(avid):
		return model.BilibiliMovie.select().where(model.BilibiliMovie.avid == avid ).limit(1).first()

	def get_first_bilibili_media(cid):
		return model.BilibiliMedia.select().where(model.BilibiliMedia.cid == cid ).limit(1).first()

	def build_bilibili_genre(bilibili, genre_name):
		genre = Alnilam.get_first_genre(genre_name)
		if genre is None:
			genre = model.Genre.create(name=genre_name)
			bilibili_genre = model.BilibiliGenre.create(bilibili=bilibili, genre=genre)
		else:
			bilibili_genre = model.BilibiliGenre.select().where(model.BilibiliGenre.bilibili == bilibili, model.BilibiliGenre.genre == genre).limit(1).first()
			if bilibili_genre is None:
				bilibili_genre = model.BilibiliGenre.create(bilibili=bilibili, genre=genre)

	def replenish_bilibili(self, avid, data, order=1):
		bilibili = Betelgeuse.get_first_bilibili(avid)
		if bilibili is not None:
			bilibili.pages = data.pages
			bilibili.save()
			bilibili_media = Betelgeuse.get_first_bilibili_media(data.cid)
			if bilibili_media is None:
				bilibili_media = model.BilibiliMedia.create(avid=avid, order=order, mid=data.mid, cid=data.cid, offsite=data.offsite,
					h5=data.h5, h5_hd=data.h5_hd, h5_low=data.h5_low, download=data.download)

	def build_bilibili(self, data, douban_id=None):
		bilibili = Betelgeuse.get_first_bilibili(data["aid"])
		if bilibili is None:
			bilibili = model.BilibiliMovie.create(douban_id=douban_id, avid=data["aid"], author=data["author"],
				typename=data["typename"], arcurl=data["arcurl"], description=data["description"], title=data["title"],
				play=data["play"])

			for tag in data["tag"].split(","):
				Betelgeuse.build_bilibili_genre(bilibili, tag)