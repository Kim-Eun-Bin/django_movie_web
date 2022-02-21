from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_main, name='movie_main'),
    path('rank', views.movie_rank, name='movie_rank'),
    path('score', views.movie_score, name='movie_score'),
    path('login', views.login, name='login'),
    path('signup', views.sign_up, name='sign_up'),
]