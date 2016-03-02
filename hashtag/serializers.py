### Author: Enrique Herreros (eherrerosj@gmail.com)
### Django assignment for EverSnap. July 2014

from hashtag.models import Album, Picture
from rest_framework import serializers


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Album serializer for the API Rest Framework
	"""
	class Meta:
		model = Album
		fields = ('hashtag', 'id')


class PictureSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Picture serializer for the API Rest Framework
	"""
	class Meta:
		model = Picture
		fields = ('id', 'url','dateup', 'datestored')