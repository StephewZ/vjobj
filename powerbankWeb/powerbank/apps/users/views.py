# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

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
			return HttpResponse(json.dumps({'data':{'nickname': user.nickname}, 'code': 0}))

def logout_view(request):
	logout(request)
	return HttpResponse(json.dumps({'data':{'url': 'login_in'}, 'code': 0}))