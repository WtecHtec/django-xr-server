from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('create', views.upload_avatar, name='create'),
  path('ocr', views.identify_ocr, name='ocr')
]