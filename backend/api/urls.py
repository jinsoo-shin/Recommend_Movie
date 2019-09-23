from django.conf.urls import url
from api.views import movie_views
from api.views import movie_poster
from api.views import auth_views
from api.views import rating_views
from api.views import js_view
from api.views import rating_views
from api.views import km_algo_views
from api.views import recommend_views
from api.views import jwb_view

urlpatterns = [
    url('auth/signup-many/$', auth_views.signup_many, name='sign_up_many'),
    url('auth/signin/$', auth_views.signin, name='sign_in'),
    url('auth/signup/$', auth_views.signup, name='sign_up'),
    url('movies/$', movie_views.movies, name='movie_list'),
    url('ratings/$', rating_views.ratings, name='rating_list'),
    url('recommends/$', recommend_views.recommends, name='recommend_list'),
    url('test/$', js_view.test, name='js_view'),
    url('km_algo/$', km_algo_views.km_algo, name='km_algo'),
    url('jwb_view/$', jwb_view.jwb_view, name='jwb_view'),
    url('delete/user/$', auth_views.delete, name='delete_user'),
    url('update/user/$', auth_views.update, name='update_user'),
    url('delete/movie/$', movie_views.delete, name='delete_movie'),
    url('update/movie/$', movie_views.update, name='update_movie'),
    url('movie_poster/$', movie_poster.poster, name='poster'),
]
