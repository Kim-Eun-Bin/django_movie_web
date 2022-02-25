import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re

from movie.models import Post, Comment


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
            movie_info_dict['code'] = re.search(r'\d+', movie_info_dict['detail_url']).group(0)
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
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.created_at = post.created_at.strftime("%Y-%m-%d")

    return render(request, 'movie/movie_review_page.html', {'post_list': posts})


def movie_review_detail(request, pk):
    post = Post.objects.filter(id=pk).values()[0]
    comment_list = Comment.objects.filter(post=pk)

    for comment in comment_list:
        comment.created_at = comment.created_at.strftime("%Y-%m-%d")

    author = User.objects.filter(id=post['author_id']).values()[0]['username']

    img_url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code=' + post['movie_id']
    img_req_header = {
        'user-agent': 'ozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    img_res = requests.get(img_url, headers=img_req_header)
    img_html = img_res.text

    url = "https://openapi.naver.com/v1/search/movie.json"

    client_id = "x0mhpyDwAQs0hQkATDat"
    client_secret = "0C7HGzonDK"

    # request header
    req_header = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    # request parameter
    req_param = {"query": post['movie_title']}
    res = requests.get(url, headers=req_header, params=req_param)

    movie_data = []
    if res.ok:
        movie = res.json()['items'][0]

        if img_res.ok:
            soup = BeautifulSoup(img_html, 'html.parser')
            img = soup.select("div.mv_info_area div.poster > a > img")
            img_resource = img[0]['src']

            if re.search(r'\d+', movie['link']).group(0) == post['movie_id']:
                movie_data.append({
                    'id': post['movie_id'],
                    'movie_title': post['movie_title'],
                    'img': img_resource,
                    'movie_year': movie['pubDate'],
                    'movie_director': str(movie['director']).replace("|", " "),
                    'movie_actor' : str(movie['actor']).replace("|", " "),
                    'movie_rating' : float(movie['userRating']) * 10
                })
    else:
        print('Error Code ', res.status_code)

    post_dict = {
        'id': post['id'],
        'title': post['title'],
        'rating': post['rating'],
        'content': str(post['content']).replace("\n", "\r\n"),
        'author': author,
        'created_at': post['created_at'].strftime("%Y-%m-%d")
    }

    return render(request, 'movie/movie_review_detail_page.html', {'post': post_dict, 'movie': movie_data[0], 'comment_list': comment_list})


def post_review(request):
    movie_id = request.GET.get("movie_id")
    movie_title = request.GET.get("movie_title")
    movie_list = {}

    if movie_id:
        url = "https://openapi.naver.com/v1/search/movie.json"

        client_id = "x0mhpyDwAQs0hQkATDat"
        client_secret = "0C7HGzonDK"

        # request header
        req_header = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        # request parameter
        req_param = {"query": movie_title}

        res = requests.get(url, headers=req_header, params=req_param)
        if res.ok:
            movies = res.json()

            data = {}
            for movie in movies['items']:
                if re.search(r'\d+', movie['link']).group(0) == movie_id:
                    data = {
                        'id': movie_id,
                        'movie_title': movie_title,
                    }

            return render(request, 'movie/post_review.html', {'movie_info': movie_list, 'selected_item': data})
        else:
            print('Error Code ', res.status_code)

    return render(request, 'movie/post_review.html', {'movie_info': movie_list})


def add_new_post(request):
    if request.method == 'POST':
        post = Post.objects.create(
            movie_id=request.POST['movie_id'],
            movie_title=request.POST['movie_title'],
            rating=request.POST['rating'],
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
            posts = Post.objects.all().order_by('-created_at')

            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': post.author.username,
                    'movie_title': post.movie_title,
                    'movie_id': post.movie_id,
                    'rating': post.rating,
                    'created_at': post.created_at.strftime('%Y-%m-%d')
                })
            return render(request, 'movie/movie_review_page.html', {'post_list': data})
        else:
            posts = Post.objects.filter(movie_title__startswith=keyword).order_by('-created_at')

            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': post.author.username,
                    'movie_title': post.movie_title,
                    'movie_id': post.movie_id,
                    'rating': post.rating,
                    'created_at': post.created_at.strftime('%Y-%m-%d')
                })
            return render(request, 'movie/movie_review_page.html', {'post_list': data})

    return render(request, 'movie/movie_review_page.html')


def search_movie(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']

        url = "https://openapi.naver.com/v1/search/movie.json"

        client_id = "x0mhpyDwAQs0hQkATDat"
        client_secret = "0C7HGzonDK"

        # request header
        req_header = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        # request parameter
        req_param = {"query": keyword, "display": 50}

        res = requests.get(url, headers=req_header, params=req_param)
        if res.ok:
            movies = res.json()

            data = []
            for movie in movies['items']:
                data.append({
                    'id': re.search(r'\d+', movie['link']).group(0),
                    'movie_title': str(movie['title']).replace("<b>", "").replace("</b>", ""),
                    'prdt_year': movie['pubDate'],
                    'director': str(movie['director']).replace("|", " ")
                })

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            print('Error Code ', res.status_code)

    return HttpResponse(json.dumps(dict), content_type='application/json')


def delete_post(request, pk):
    post = Post.objects.filter(id=pk)
    post.delete()

    return redirect('/movie/review_list')


def edit_post(request, pk):
    post = Post.objects.filter(id=pk).values()[0]
    selected_item = {
        'id': post['movie_id'],
        'movie_title': post['movie_title']
    }

    return render(request, 'movie/edit_post_review.html', {'selected_item': selected_item, 'edit_post': post})


def edit_post_save(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.rating = request.POST['rating']
    post.title = request.POST['title']
    post.content = request.POST['content']

    post.save()

    return redirect('/movie/review_list')


def add_comment(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            text=request.POST['comment-content']
        )

        comment.save()

        return redirect('movie_review_detail', pk=pk)

    return redirect('movie_review_detail', pk=pk)


def delete_comment(request, pk):
    comments = Comment.objects.filter(pk=pk).values()[0]
    post_id = comments['post_id']

    comment = Comment.objects.get(pk=pk)
    comment.delete()

    return redirect('movie_review_detail', pk=post_id)


def my_page(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    for post in posts:
        post.created_at = post.created_at.strftime("%Y-%m-%d")

    return render(request, 'movie/my_page.html', {'post_list': posts})