from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_main, name='movie_main'),
    path('rank/reservation', views.movie_rank_reservation, name='movie_rank_reservation'),
    path('rank/release', views.movie_rank_release, name='movie_rank_release'),
    path('rank/rating', views.movie_rank_rating, name='movie_rank_rating'),
    path('rank/like', views.movie_rank_like, name='movie_rank_like'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_sign_up, name='sign_up'),
    path('logout', views.user_logout, name='user_logout'),
    path('review_list', views.movie_review_list, name='movie_review_list'),
    path('review_list/post', views.post_review, name='post_review'),
    path('review_list/post/add', views.add_new_post, name='add_new_post'),
    path('review_list/search', views.search_review, name='search_review'),
    path('review_list/post/add/search', views.search_movie, name='search_movie'),
]

