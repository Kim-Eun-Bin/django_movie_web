from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.utils import timezone


def login(request):

    return render(request, 'movie/login_page.html')


def sign_up(request):

    return render(request, 'movie/signup_page.html')


def movie_main(request):

    return render(request, 'movie/main_page.html')


def movie_rank(request):

    return render(request, 'movie/movie_rank_page.html')


def movie_score(request):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    key = "be35b97e5763c4cc4fcf49c888de0390"

    req_param = {"key": key}

    res = requests.get(url, params=req_param)
    html = res.text

    if res.ok:
        soup = BeautifulSoup(html, 'html.parser')

        return render(request, 'movie/movie_score_page.html', {'movie': soup.text})
    else:
        print('Error Code ', res.status_code)