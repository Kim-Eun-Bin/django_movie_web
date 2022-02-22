from django.db import models
from django.utils import timezone


class Movie_info(models.Model):
    # 제목
    movie_title = models.TextField()
    # 제작 연도
    prdt_year = models.TextField()
    # 장르
    genre = models.TextField()
    # 감독
    director = models.TextField()

    def __str__(self):
        return self.movie_title


class Post(models.Model):
    movie_id = models.ForeignKey("Movie_info", related_name="movie_info", on_delete=models.CASCADE, db_column="movie_id")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
