from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('writings', views.writings, name='writings'),
    path('keywords', views.keywords, name='keywords'),
    path('recommendations', views.recommendations, name='recommendations'),
    path('write', views.write, name='write'),
    path('delete', views.delete, name='delete'),
]
