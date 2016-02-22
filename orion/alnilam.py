import model.db as model

class Alnilam:

	def __init__(self):
		pass

	def get_first_movie(douban_id):
 		return model.Movie.select().where(model.Movie.douban_id == douban_id).limit(1)[0]

	def get_first_contry(name):
		return model.Country.select().where(model.Country.name == name).limit(1)[0]

	def build_country(movie, country_name):
		country = Alnilam.get_first_contry(country_name)
		if country is None:
			country = model.Country.create(name=country_name)
			movie_country = model.MovieCountry.create(movie_id=movie.id, country_id=country.id)
		else:
			movie_country = model.MovieCountry.select().where(model.MovieCountry.movie == movie, model.MovieCountry.country == country).limit(1)[0]
			if movie_country is None:
				movie_country = model.MovieCountry.create(movie_id=movie.id, country_id=country.id)

	def get_first_genre(name):
		return model.Genre.select().where(model.Genre.name == name).limit(1)[0]

	def build_genre(movie, genre_name):
		genre = Alnilam.get_first_genre(genre_name)
		if genre is None:
			genre = model.Genre.create(name=genre_name)
			movie_genre = model.MovieGenre.create(movie_id=movie.id, genre_id=genre.id)
		else:
			movie_genre = model.MovieGenre.select().where(model.MovieGenre.movie == movie, model.MovieGenre.genre == genre).limit(1)[0]
			if movie_genre is None:
				movie_genre = model.MovieGenre.create(movie_id=movie.id, genre_id=genre.id)


	def get_first_celebrity(douban_id):
		return model.Celebrity.select().where(model.Celebrity.douban_id == douban_id).limit(1)[0]

	def build_movie_director(movie, director):
		movie_director = model.MovieDirector.select().where(model.MovieDirector.movie == movie, model.MovieDirector.director == director).limit(1)[0]
		if movie_director is None:
			model.MovieDirector.create(movie_id=movie.id, director_id=director.id)

	def build_movie_cast(movie, cast):
		movie_cast = model.MovieCast.select().where(model.MovieCast.movie == movie, model.MovieCast.cast == cast).limit(1)[0]
		if movie_cast is None:
			model.MovieCast.create(movie_id=movie.id, cast_id=cast.id)

	def build_celebrity(douban_id, name, douban_url, images, build_relationship):
		celebrity = Alnilam.get_first_celebrity(douban_id)
		if celebrity is None:
			celebrity = model.Celebrity.create(douban_id=douban_id, name=name, douban_url=douban_url)
			Image.create(small=images['small'], medium=images['medium'], large=images['large'], item_type=celebrity.__class_name__, item_id = celebrity.id)

		Alnilam.build_relationship(movie, celebrity)

	def generate_movie(self, movie_sub, detail):
		movie = Alnilam.get_first_movie(detail.id)
		if movie is None:
			movie = model.Movie.create(douban_id=detail.id, title=detail.title, douban_url=movie_sub.url, rate=movie_sub.rate, year=detail.year, douban_mobile_url=detail.mobile_url,
						ratings_count=detail.ratings_count, summary=detail.summary, original_title=detail.original_title)
			Image.create(small=detail.images['small'], medium=detail.images['medium'], large=detail.images['large'], item_type=movie.__class_name__, item_id = movie.id)

			for country_name in detail.countries:
				Alnilam.build_country(movie, country_name)

			for genre_name in detail.genres:
				Alnilam.build_genre(movie, genre_name)

			for director_json in detail.directors:
				Alnilam.build_celebrity(director_json["id"], director_json["name"], director_json["alt"], director_json["avatars"], build_movie_director)

			for cast_json in detail.casts:
				Alnilam.build_celebrity(cast_json["id"], cast_json["name"], cast_json["alt"], director_json["avatars"], build_movie_cast)

