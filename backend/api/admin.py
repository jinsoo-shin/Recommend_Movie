from django.contrib import admin

from . models import Profile,Rating,Movie,KmeansResult,Poster,Subscribe

admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(KmeansResult)
admin.site.register(Poster)
admin.site.register(Subscribe)
