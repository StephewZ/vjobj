# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F,Q

import json
from datetime import datetime

from users.models import users, institutions, status_user, status_module

def getData(user, pS, cP, sN, oT, mX):
	datas = ''
	return datas

@login_required
@csrf_exempt
def statusList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'statusList':
			status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
			if status_module.objects.filter(status_id__in = status_id_list, module_id = 11).exists():
				code = 0
				msg = getData(user, params['pageSize'], params['currentPage'], params['sortName'], params['orderType'], params['mixing'])
			else:
				msg = 'denied'
				code = 404
			return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def statusAdd(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'statusAdd':
		status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
		if status_module.objects.filter(status_id__in = status_id_list, module_id = 8).exists():
			code = 0
			err = ''
		else:
			msg = 'denied'
			code = 404	
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code, 'err': err}))

@login_required
@csrf_exempt
def statusDel(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'userDel':
		status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
		if status_module.objects.filter(status_id__in = status_id_list, module_id = 9).exists():
			code = 0
			err = ''
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def statusEdit(request):
	code = 1
	msg = ''
	return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))		