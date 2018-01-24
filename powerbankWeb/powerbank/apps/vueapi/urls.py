# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import main, inst
from users.views import user_login, get_userinfo, logout_view
from django.views.generic import TemplateView

app_name = 'root'

urlpatterns = [
	url(r'^$', main.main_view, name="home"),
	url(r'^login_in/$', user_login, name="login_in"),
	url(r'^userinfo/$', get_userinfo, name="userinfo"),
	url(r'^logout/$', logout_view, name="logout"),
	url(r'^index/$', main.index, name="index"),
	url(r'^instList/$', inst.instList, name="instList")
	]