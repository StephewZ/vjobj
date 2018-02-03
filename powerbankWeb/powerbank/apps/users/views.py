# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from vueapi.views.permit import Authentication

import json

@csrf_exempt
def user_login(request):
	if request.method == 'GET':
		error_msg = request.GET.get("error_msg", None)
		return render(request, 'login.html', {'error_msg': error_msg})

	if request.method == 'POST':
		username = request.POST.get('useradmin', None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password = password)
		if user is not None and user.is_delete == 0:
			login(request, user)
			return HttpResponseRedirect(reverse('root:home'))
		else:
			return HttpResponseRedirect(reverse('login') + "error_msg=用户名和密码不匹配!")

@csrf_exempt
@login_required
def get_userinfo(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		if params['tip'] == 'nickname':
			leftItem = {}
			leftItem['one'] = {}
			leftItem['one']['show'] = False
			for item in ['instIndex', 'userIndex', 'statusIndex']:
				if Authentication(item, user):
					leftItem['one']['show'] = True
					leftItem['one'][item] = True
				else:
					leftItem['one'][item] = False

			leftItem['two'] = {}
			leftItem['two']['show'] = False

			for item in ['deviceIndex']:
				if Authentication(item, user):
					leftItem['two']['show'] = True
					leftItem['two'][item] = True
				else:
					leftItem['two'][item] = False

			leftItem['three'] = {}
			leftItem['three']['show'] = False

			for item in ['orderIndex', 'customerIndex', 'achieveIndex']:
				if Authentication(item, user):
					leftItem['three']['show'] = True
					leftItem['three'][item] = True
				else:
					leftItem['three'][item] = False
			return HttpResponse(json.dumps({'data':{'nickname': user.nickname, 'leftItem': leftItem}, 'code': 0}))

@csrf_exempt
@login_required
def set_info(request):
	code = 0
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		if params['tip'] == 'userSet':
			user = authenticate(username = user.username, password = params['pass'])
		if user is None:
			code = 2
			err = '用户密码输入错误！'
		elif params['newPass'] != params['checkPass']:
			code = 2
			err = '两次输入的新密码不一致！'
		elif len(params['newPass']) > 15:
			code = 2
			err = '密码长度超过限制！'
		else:
			err = '修改成功！'
			user.set_password(params['newPass'])
			user.save()	
		return HttpResponse(json.dumps({'data': {'err': err}, 'code': code}))

def logout_view(request):
	logout(request)
	return HttpResponse(json.dumps({'data':{'url': 'login_in'}, 'code': 0}))