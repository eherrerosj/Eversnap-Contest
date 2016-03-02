### Author: Enrique Herreros (eherrerosj@gmail.com)
### Django assignment for EverSnap. July 5th, 2014

from django.shortcuts import render
from django.http import HttpResponse
from tasks import searchpics
import hashtag.models
from hashtag.models import Album, Picture
from django.template import Context, loader 
from rest_framework import viewsets
from hashtag.serializers import AlbumSerializer, PictureSerializer

# Use albums.html template (Galleriffic jQuery album viewer)
#	Send all pictures in DB.
def showalbums(request, template="albums.html"):
	albums = Album.objects.all()
	context = {'oldestpicture': Picture.objects.order_by("-datestored")[0],
	'pictures': Picture.objects.select_related('Album').order_by("album").all()[1:]}
	return render(request, template, context)

# Use mostpopular.html template (AutomaticImageMontage jQuery auto collage creator)
#	Send top 7 pictures (most favourited)
def mostpopular(request, template="mostpopular.html"):
	albums = Album.objects.all()
	context = {'top7' : Picture.objects.order_by('-likes')[1:8]}
	return render(request, template, context)

# Serialize Albums for REST
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# Serialize Pictures for REST
class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer