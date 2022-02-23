import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Movie_info
from datetime import date


def user_logout(request):
    logout(request)

    return redirect('/movie')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/movie')
        else:
            return render(request, 'movie/login_page.html')
    else:
        return render(request, 'movie/login_page.html')


def user_sign_up(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_check']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'])

            user.save()
            return redirect('/movie/login')

    return render(request, 'movie/signup_page.html')


def movie_main(request):
    return render(request, 'movie/main_page.html')


def movie_rank_like(request):
    url = 'https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=likeCount'
    req_header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
    }

    res = requests.get(url, headers=req_header)
    html = res.text

    if res.ok:
        soup = BeautifulSoup(html, 'html.parser')
        img_list = soup.select("div.thumb img[src]")
        age_list = soup.select("dt.tit span")
        title_list = soup.select("dt.tit a")
        rating_list = soup.select("div.star_t1 a > span.num")

        outline_list = soup.select("dl.info_txt1 dd")
        outline_list_dt = soup.select("dl.info_txt1 dt")

        genre_list = []
        director_list = []
        actor_list = []

        i = 0
        while i < len(outline_list_dt):
            genre_list.append(outline_list[i].text)

            if i + 1 < len(outline_list_dt):
                director_list.append(outline_list[i + 1].text)

            if i + 2 < len(outline_list_dt) and outline_list_dt[i + 2].text == '출연':
                actor_list.append(outline_list[i + 2].text)
                i += 3
            else:
                actor_list.append('')
                i += 2

        movie_info_list = []

        for i in range(len(title_list)):
            movie_info_dict = {}

            movie_info_dict['title'] = title_list[i].text
            movie_info_dict['detail_url'] = title_list[i]['href']
            movie_info_dict['age'] = age_list[i].text
            movie_info_dict['img'] = img_list[i]['src']
            movie_info_dict['rating'] = rating_list[i].text
            movie_info_dict['genre'] = genre_list[i]
            movie_info_dict['director'] = director_list[i]
            movie_info_dict['actor'] = actor_list[i]
            movie_info_dict['rating_percent'] = float(rating_list[i].text) * 10

            movie_info_list.append(movie_info_dict)

        page = request.GET.get("page", 1)
        paginator = Paginator(movie_info_list, per_page=10, orphans=5)

        movies = paginator.page(int(page))

    return render(request, 'movie/movie_rank_like.html', {'movie_info': movies})


def movie_rank_rating(request):
    url = 'https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=point'
    req_header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
    }

    res = requests.get(url, headers=req_header)
    html = res.text

    if res.ok:
        soup = BeautifulSoup(html, 'html.parser')
        img_list = soup.select("div.thumb img[src]")
        age_list = soup.select("dt.tit span")
        title_list = soup.select("dt.tit a")
        rating_list = soup.select("div.star_t1 a > span.num")

        outline_list = soup.select("dl.info_txt1 dd")
        outline_list_dt = soup.select("dl.info_txt1 dt")

        genre_list = []
        director_list = []
        actor_list = []

        i = 0
        while i < len(outline_list_dt):
            genre_list.append(outline_list[i].text)

            if i + 1 < len(outline_list_dt):
                director_list.append(outline_list[i + 1].text)

            if i + 2 < len(outline_list_dt) and outline_list_dt[i + 2].text == '출연':
                actor_list.append(outline_list[i + 2].text)
                i += 3
            else:
                actor_list.append('')
                i += 2

        movie_info_list = []

        for i in range(len(title_list)):
            movie_info_dict = {}

            movie_info_dict['title'] = title_list[i].text
            movie_info_dict['detail_url'] = title_list[i]['href']
            movie_info_dict['age'] = age_list[i].text
            movie_info_dict['img'] = img_list[i]['src']
            movie_info_dict['rating'] = rating_list[i].text
            movie_info_dict['genre'] = genre_list[i]
            movie_info_dict['director'] = director_list[i]
            movie_info_dict['actor'] = actor_list[i]
            movie_info_dict['rating_percent'] = float(rating_list[i].text) * 10

            movie_info_list.append(movie_info_dict)

        page = request.GET.get("page", 1)
        paginator = Paginator(movie_info_list, per_page=10, orphans=5)

        movies = paginator.page(int(page))

    return render(request, 'movie/movie_rank_rating.html', {'movie_info': movies})


def movie_rank_release(request):
    url = 'https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=open'
    req_header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
    }

    res = requests.get(url, headers=req_header)
    html = res.text

    if res.ok:
        soup = BeautifulSoup(html, 'html.parser')
        img_list = soup.select("div.thumb img[src]")
        age_list = soup.select("dt.tit span")
        title_list = soup.select("dt.tit a")
        rating_list = soup.select("div.star_t1 a > span.num")

        outline_list = soup.select("dl.info_txt1 dd")
        outline_list_dt = soup.select("dl.info_txt1 dt")

        genre_list = []
        director_list = []
        actor_list = []

        i = 0
        while i < len(outline_list_dt):
            genre_list.append(outline_list[i].text)

            if i + 1 < len(outline_list_dt):
                director_list.append(outline_list[i + 1].text)

            if i + 2 < len(outline_list_dt) and outline_list_dt[i + 2].text == '출연':
                actor_list.append(outline_list[i + 2].text)
                i += 3
            else:
                actor_list.append('')
                i += 2

        movie_info_list = []

        for i in range(len(title_list)):
            movie_info_dict = {}

            movie_info_dict['title'] = title_list[i].text
            movie_info_dict['detail_url'] = title_list[i]['href']
            movie_info_dict['age'] = age_list[i].text
            movie_info_dict['img'] = img_list[i]['src']
            movie_info_dict['rating'] = rating_list[i].text
            movie_info_dict['genre'] = genre_list[i]
            movie_info_dict['director'] = director_list[i]
            movie_info_dict['actor'] = actor_list[i]
            movie_info_dict['rating_percent'] = float(rating_list[i].text) * 10

            movie_info_list.append(movie_info_dict)

        page = request.GET.get("page", 1)
        paginator = Paginator(movie_info_list, per_page=10, orphans=5)

        movies = paginator.page(int(page))

    return render(request, 'movie/movie_rank_release.html', {'movie_info': movies})


def movie_rank_reservation(request):
    url = 'https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=reserve'
    req_header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
    }

    res = requests.get(url, headers=req_header)
    html = res.text

    if res.ok:
        soup = BeautifulSoup(html, 'html.parser')
        img_list = soup.select("div.thumb img[src]")
        age_list = soup.select("dt.tit span")
        title_list = soup.select("dt.tit a")
        rating_list = soup.select("div.star_t1 a > span.num")

        outline_list = soup.select("dl.info_txt1 dd")
        outline_list_dt = soup.select("dl.info_txt1 dt")

        genre_list = []
        director_list = []
        actor_list = []

        i = 0
        while i < len(outline_list_dt):
            genre_list.append(outline_list[i].text)

            if i+1 < len(outline_list_dt):
                director_list.append(outline_list[i+1].text)

            if i+2 < len(outline_list_dt) and outline_list_dt[i+2].text == '출연':
                actor_list.append(outline_list[i+2].text)
                i += 3
            else:
                actor_list.append('')
                i += 2

        movie_info_list = []

        for i in range(len(title_list)):
            movie_info_dict = {}

            movie_info_dict['title'] = title_list[i].text
            movie_info_dict['detail_url'] = title_list[i]['href']
            movie_info_dict['age'] = age_list[i].text
            movie_info_dict['img'] = img_list[i]['src']
            movie_info_dict['rating'] = rating_list[i].text
            movie_info_dict['genre'] = genre_list[i]
            movie_info_dict['director'] = director_list[i]
            movie_info_dict['actor'] = actor_list[i]
            movie_info_dict['rating_percent'] = float(rating_list[i].text) * 10

            movie_info_list.append(movie_info_dict)

        page = request.GET.get("page", 1)
        paginator = Paginator(movie_info_list, per_page=10, orphans=5)

        movies = paginator.page(int(page))

        return render(request, 'movie/movie_rank_reservation.html', {'movie_info': movies})


def movie_review_list(request):
    # url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    # key = "be35b97e5763c4cc4fcf49c888de0390"
    #
    # req_param = {"key": key, 'itemPerPage': 100}
    #
    # res = requests.get(url, params=req_param)
    #
    # if res.ok:
    #     movie_list = res.json()['movieListResult']['movieList']
    #
    #     for item in movie_list:
    #         if item['directors']:
    #             item['directors'] = item['directors'][0]['peopleNm']
    #         else:
    #             item['directors'] = ''
    #
    #     for item in movie_list:
    #         if "성인물" not in item['genreAlt']:
    #             movie = Movie_info.objects.create(
    #                 movie_title=item['movieNm'],
    #                 prdt_year=item['prdtYear'],
    #                 genre=item['genreAlt'],
    #                 director=item['directors'],
    #             )
    #             movie.save()
    #
    #     return render(request, 'movie/movie_review_page.html')
    # else:
    #     print('Error Code ', res.status_code)
    posts = Post.objects.all()

    for post in posts:
        post.created_at = post.created_at.strftime("%Y-%m-%d")

    return render(request, 'movie/movie_review_page.html', {'post_list': posts})


def post_review(request):
    movie_list = Movie_info.objects.all().order_by('movie_title')
    movie_id = request.GET.get("movie")

    if movie_id:
        movie = Movie_info.objects.filter(id=movie_id).values()[0]
        return render(request, 'movie/post_review.html', {'movie_info': movie_list, 'selected_item': movie})

    return render(request, 'movie/post_review.html', {'movie_info': movie_list})


def add_new_post(request):
    if request.method == 'POST':
        movie = Movie_info.objects.get(pk=request.POST['movie_id'])

        post = Post.objects.create(
            movie_id=movie,
            author=request.user,
            title=request.POST['title'],
            content=request.POST['content'],
        )

        post.save()
        return redirect('/movie/review_list')

    return render(request, 'movie/post_review.html')


def search_review(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']

        if keyword == "all":
            posts = Post.objects.all()

            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': post.author.username,
                    'movie_title': post.movie_id.movie_title,
                    'created_at': post.created_at.strftime('%Y-%m-%d')
                })
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            posts = Post.objects.filter(movie_id__movie_title__startswith=keyword)

            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': post.author.username,
                    'movie_title': post.movie_id.movie_title,
                    'created_at': post.created_at.strftime('%Y-%m-%d')
                })
            return HttpResponse(json.dumps(data), content_type='application/json')

    return render(request, 'movie/movie_review_page.html')


def search_movie(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']

        if keyword == "all":
            movies = Movie_info.objects.all().order_by('movie_title')

            data = []
            for movie in movies:
                data.append({
                    'id': movie.id,
                    'movie_title': movie.movie_title,
                    'prdt_year': movie.prdt_year,
                    'genre': movie.genre,
                    'director': movie.director
                })
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            movies = Movie_info.objects.filter(movie_title__startswith=keyword).order_by('movie_title')

            data = []
            for movie in movies:
                data.append({
                    'id': movie.id,
                    'movie_title': movie.movie_title,
                    'prdt_year': movie.prdt_year,
                    'genre': movie.genre,
                    'director': movie.director
                })
            return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(dict), content_type='application/json')

