from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # id = models.IntegerField(unique=True,primary_key=True,default=number)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default='M')
    age = models.IntegerField(default=25)
    occupation = models.CharField(max_length=200)

def number(self):
    num = Profile.objects.count()
    if num == None:
        return 1
    else:
        return num + 1


#  wrapper for create user Profile
def create_profile(**kwargs):

    user = User.objects.create_user(
        username=kwargs['username'],
        password=kwargs['password'],
        is_active=True,
    )

    profile = Profile.objects.create(
        user=user,
        gender=kwargs['gender'],
        age=kwargs['age'],
        occupation=kwargs['occupation']
    )

    return profile


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=500)
    viewCnt = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    @property
    def genres_array(self):
        return self.genres.strip().split('|')

class Rating(models.Model):
    # profile = models.ForeignKey(Profile, to_field='id', db_column='username', on_delete=models.CASCADE)
    # username = models.CharField(max_length=200)
    # userid = models.ForeignKey(Profile, db_column='userid',to_field='id', on_delete=models.CASCADE)

    userid = models.IntegerField(default=0)
    movieid = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True)

class Subscribe(models.Model):
    user_id = models.IntegerField(primary_key=True)
    expiration = models.CharField(max_length=100)

class KmeansResult(models.Model):
    clusterlist = models.CharField(max_length=20000)

class SimilarUsers(models.Model):
    users = models.CharField(max_length=20000)

class SimilarMovies(models.Model):
    movies = models.CharField(max_length=20000)


class AlgorithmResult(models.Model):
    name = models.CharField(max_length=500)#모델 이름
    value = models.CharField(max_length=20000)


class Poster(models.Model):
    id = models.IntegerField(primary_key=True)
    imdbId = models.IntegerField()
    posterUrl = models.CharField(max_length=20000)

