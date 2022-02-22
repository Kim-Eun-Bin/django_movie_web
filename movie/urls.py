from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_main, name='movie_main'),
    path('rank/reservation', views.movie_rank_reservation, name='movie_rank_reservation'),
    path('rank/release', views.movie_rank_release, name='movie_rank_release'),
    path('rank/rating', views.movie_rank_rating, name='movie_rank_rating'),
    path('rank/like', views.movie_rank_like, name='movie_rank_like'),
    path('post', views.movie_post, name='movie_post'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_sign_up, name='sign_up'),
    path('', views.user_logout, name='logout'),
    path('post/add', views.new_post, name='add_post'),
]