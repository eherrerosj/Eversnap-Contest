### Author: Enrique Herreros (eherrerosj@gmail.com)
### Django assignment for EverSnap. July 2014

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from hashtag.models import Album, Picture
from rest_framework import viewsets, routers

#Not needed in Django 1.7+
admin.autodiscover()

from hashtag import views

# ViewSets define the view behavior
class AlbumViewSet(viewsets.ModelViewSet):
    model = Album

class PictureViewSet(viewsets.ModelViewSet):
    model = Picture


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'pictures', PictureViewSet)

#Map URL URI patterns - views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ever.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^showalbums/', 'hashtag.views.showalbums'),
    url(r"^mostpopular/", 'hashtag.views.mostpopular'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^pictures/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^albums/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    
)
