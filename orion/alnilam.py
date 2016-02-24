import model.db as model

class Alnilam:

	def __init__(self):
		pass

	def get_first_movie(douban_id):
 		return model.Movie.select().where(model.Movie.douban_id == douban_id).limit(1).first()

	def get_first_contry(name):
		return model.Country.select().where(model.Country.name == name).limit(1).first()

	def build_country(movie, country_name):
		country = Alnilam.get_first_contry(country_name)
		if country is None:
			country = model.Country.create(name=country_name)
			movie_country = model.MovieCountry.create(movie=movie, country=country)
		else:
			movie_country = model.MovieCountry.select().where(model.MovieCountry.movie == movie, model.MovieCountry.country == country).limit(1).first()
			if movie_country is None:
				movie_country = model.MovieCountry.create(movie=movie, country=country)

	def get_first_genre(name):
		return model.Genre.select().where(model.Genre.name == name).limit(1).first()

	def build_genre(movie, genre_name):
		genre = Alnilam.get_first_genre(genre_name)
		if genre is None:
			genre = model.Genre.create(name=genre_name)
			movie_genre = model.MovieGenre.create(movie=movie, genre=genre)
		else:
			movie_genre = model.MovieGenre.select().where(model.MovieGenre.movie == movie, model.MovieGenre.genre == genre).limit(1).first()
			if movie_genre is None:
				movie_genre = model.MovieGenre.create(movie=movie, genre=genre)


	def get_first_celebrity(douban_id):
		return model.Celebrity.select().where(model.Celebrity.douban_id == douban_id).limit(1).first()

	def build_movie_director(movie, director):
		movie_director = model.MovieDirector.select().where(model.MovieDirector.movie == movie, model.MovieDirector.director == director).limit(1).first()
		if movie_director is None:
			model.MovieDirector.create(movie=movie, director=director)

	def build_movie_cast(movie, cast):
		movie_cast = model.MovieCast.select().where(model.MovieCast.movie == movie, model.MovieCast.cast == cast).limit(1).first()
		if movie_cast is None:
			model.MovieCast.create(movie=movie, cast=cast)

	def build_celebrity(movie, douban_id, name, douban_url, images, build_relationship):
		celebrity = Alnilam.get_first_celebrity(douban_id)
		if celebrity is None:
			celebrity = model.Celebrity.create(douban_id=douban_id, name=name, douban_url=douban_url)
			model.Image.create(small=images['small'], medium=images['medium'], large=images['large'], item_type=celebrity.__class__.__name__, item_id = celebrity.id)

		build_relationship(movie, celebrity)

	def generate_movie(self, detail):
		movie = Alnilam.get_first_movie(detail.id)
		if movie is None:
			movie = model.Movie.create(douban_id=detail.id, title=detail.title, douban_url=detail.alt, rate=detail.rating["average"], year=detail.year, douban_mobile_url=detail.mobile_url,
						ratings_count=detail.ratings_count, summary=detail.summary, original_title=detail.original_title, collect_count=detail.collect_count, reviews_count=detail.reviews_count)
			model.Image.create(small=detail.images['small'], medium=detail.images['medium'], large=detail.images['large'], item_type=movie.__class__.__name__, item_id = movie.id)

			for country_name in detail.countries:
				Alnilam.build_country(movie, country_name)

			for genre_name in detail.genres:
				Alnilam.build_genre(movie, genre_name)

			for director_json in detail.directors:
				if director_json["id"] is not None:
					Alnilam.build_celebrity(movie, director_json["id"], director_json["name"], director_json["alt"], director_json["avatars"], Alnilam.build_movie_director)

			for cast_json in detail.casts:
				if cast_json["id"] is not None:
					Alnilam.build_celebrity(movie, cast_json["id"], cast_json["name"], cast_json["alt"], cast_json["avatars"], Alnilam.build_movie_cast)

