from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
# from . import views as core_views
from . import views
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import re_path



urlpatterns = [


    path('', views.starting_page, name="starting-page"),

    path('registration/', views.signup, name="registration-page"),
    path('login/', views.user_login, name="login-page"),
    path('zapisz/', views.zapisz, name="zapisz-page"),
    path('wybierzklase/', views.chooseclas, name="chooseclas-page"),
    path('zmiendane/', views.zmiendane, name="zmiendane-page"),
    path('zmienklase/', views.zmienclas, name="zmienclas-page"),
    path('zmienstatus/', views.zmienstatus, name="zmienstatus-page"),
    path('zestawienieklasy/', views.zestawienieklasy, name="zestawienieklasy-page"),
    path('zestawienie/', views.zestawienie, name="zestawienie-page"),
    path('uploadfile/', views.uploadfile, name="uploadfile-page"),
    path('ogloszenia/', views.readposts, name="readposts-page"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
          views.activate, name='activate'),

]


admin.site.site_header = 'Rekrutacja 2023'                    # default: "Django Administration"
admin.site.index_title = 'Rekrutacja 2023'                 # default: "Site administration"
admin.site.site_title = 'Rekrutacja 2023' # default: "Django site admin"
