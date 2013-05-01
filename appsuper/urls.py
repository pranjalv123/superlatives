from django.conf.urls import patterns, url

from appsuper import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'superlatives/$', views.getSuperlatives, name='index'),
    url(r'selections/$', views.getSelections, name='index'),
    url(r'newSuperlative/$', views.newSuperlative, name='index'),
    url(r'updateSuperlative/$', views.updateSuperlative, name='index'),
    url(r'updateSelection/$', views.updateSelection, name='index'),
    url(r'deleteSuperlative/$', views.deleteSuperlative, name='index'),
)
