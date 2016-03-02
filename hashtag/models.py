### Author: Enrique Herreros (eherrerosj@gmail.com)
### Django assignment for EverSnap. July 5th, 2014

from django.db import models
import datetime


class Album(models.Model):
	hashtag = models.CharField(max_length=200, unique=True)	# the name of the album is the hashtag to be fetched

class Picture(models.Model):
    id = models.AutoField(primary_key=True)  # autoincrease
    tweet_id = models.BigIntegerField(unique=True)  # store the tweet ID. For bypassing the 100 purposes
    url = models.URLField(unique=True)	# URL URI string
    dateup = models.DateTimeField(auto_now=False, auto_now_add=False)	# picture uploaded to Twitter, date
    datestored = models.DateTimeField(auto_now=False, auto_now_add=False)	# picture fetched by our app, date 
    owner = models.CharField(max_length=20)	# account name of the uploader
    likes = models.PositiveIntegerField()	# number of times picture favourited
    album = models.ForeignKey(Album)	# album to which this picture belongs (hashtag)