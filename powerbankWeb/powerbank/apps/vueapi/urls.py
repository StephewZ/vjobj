# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import main, inst, user, status, device
from .pay import wxpay
from users.views import user_login, get_userinfo, logout_view, set_info
from django.views.generic import TemplateView

app_name = 'root'

urlpatterns = [
	url(r'^login_in/$', user_login, name="login_in"),
	url(r'^userinfo/$', get_userinfo, name="userinfo"),
	url(r'^userSet/$', set_info, name="setInfo"),
	url(r'^logout/$', logout_view, name="logout"),
	url(r'^index/$', main.index, name="index"),
	url(r'^instList/$', inst.instList, name="instList"),
	url(r'^instAdd/$', inst.instAdd, name="instAdd"),
	url(r'^instDel/$', inst.instDel, name="instDel"),
	url(r'^instEdit/$', inst.instEdit, name="instEdit"),
	url(r'^userList/$', user.userList, name="userList"),
	url(r'^userAdd/$', user.userAdd, name="userAdd"),
	url(r'^userDel/$', user.userDel, name="userDel"),
	url(r'^userEdit/$', user.userEdit, name="userEdit"),
	url(r'^statusList/$', status.statusList, name="statusList"),
	url(r'^statusAdd/$', status.statusAdd, name="statusAdd"),
	url(r'^statusDel/$', status.statusDel, name="statusDel"),
	url(r'^statusEdit/$', status.statusEdit, name="statusEdit"),
	url(r'^paydetail', wxpay.paydetail, name="paydetail"),
	url(r'^deviceList/$', device.deviceList, name="deviceList"),
	url(r'^deviceAdd/$', device.deviceAdd, name="deviceAdd"),
	url(r'^deviceDel/$', device.deviceDel, name="deviceDel"),
	url(r'^deviceEdit/$', device.deviceEdit, name="deviceEdit"),
	url(r'', main.main_view, name="home"),
	]