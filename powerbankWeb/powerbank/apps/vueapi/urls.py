# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import main, inst, user, status, device, wx, goods, goods_pipe,send
from .pay import wxpay
from users.views import user_login, get_userinfo, logout_view, set_info
from django.views.generic import TemplateView

app_name = 'root'

urlpatterns = [
	url(r'^pay/re_paying/', wx.paydetail, name="pay"),
	# url(r'^pay/paying/', main.pay, name="pay"),
	url(r'^paydetail', wx.pay, name="paydetail"),
	url(r'^payinfo$', wx.payinfo, name="payinfo"),
	url(r'^pay/payback_url$', main.payback_url, name="payback_url"),
	url(r'^sendMQ$', send.sendMQ, name="sendMQ"),
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
	url(r'^deviceList/$', device.deviceList, name="deviceList"),
	url(r'^deviceAdd/$', device.deviceAdd, name="deviceAdd"),
	url(r'^deviceDel/$', device.deviceDel, name="deviceDel"),
	url(r'^deviceEdit/$', device.deviceEdit, name="deviceEdit"),
	url(r'^goodsList/$', goods.goodsList, name="goodsList"),
	url(r'^goodsAdd/$', goods.goodsAdd, name="goodsAdd"),
	url(r'^goodsDel/$', goods.goodsDel, name="goodsDel"),
	url(r'^goodsEdit/$', goods.goodsEdit, name="goodsEdit"),
	url(r'^goods_pipeList/$', goods_pipe.goods_pipeList, name="goods_pipeList"),
	url(r'^goods_pipeAdd/$', goods_pipe.goods_pipeAdd, name="goods_pipeAdd"),
	url(r'^goods_pipeDel/$', goods_pipe.goods_pipeDel, name="goods_pipeDel"),
	url(r'^goods_pipeEdit/$', goods_pipe.goods_pipeEdit, name="goods_pipeEdit"),
	url(r'^main_view1/$', main.main_view1, name="home1"),
	url(r'', main.main_view, name="home"),
	]