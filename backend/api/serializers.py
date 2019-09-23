from .models import Profile, Movie, Rating, KmeansResult, SimilarMovies, SimilarUsers, Subscribe
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.SerializerMethodField('get_username')
    is_staff = serializers.SerializerMethodField('get_is_staff')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'is_staff', 'gender', 'age', 'occupation')

    def get_username(self, obj):
        return obj.user.username

    def get_is_staff(self, obj):
        return obj.user.is_staff


class MovieSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array','viewCnt','rating')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('userid', 'movieid', 'rating','date')

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('user_id', 'expiration')


class KmeansResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KmeansResult
        # fields = ('clusterlist')
        fields = '__all__'

class SimilarUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarUsers
        fields = '__all__'

class SimilarMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarMovies
        fields = '__all__'