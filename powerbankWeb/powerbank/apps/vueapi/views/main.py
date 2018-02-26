# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .permit import Authentication

import json

from users.models import users, institutions, status_user, status_module

@login_required
def main_view1(request):
	return render(request, 'index.html')

def main_view(request):
	code = request.GET.get('code', None)
	device = request.GET.get('device', None)
	if code != None and device != None:
		return render(request, 'index.html')
	else:
		return HttpResponseRedirect('/main_view1/')

def pay(request):
	code = request.GET.get('code')
	device = request.GET.get('device').strip('/\\')
	return HttpResponseRedirect('/pay/paying/?device=' + device + '&code=' + code)

def payback_url(request):
    return render(request, 'paydetail.html', {'request': 'ok'})

@login_required
@csrf_exempt
def index(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		options = ''
		code = 1
		if params['tip'] in ['instIndex', 'userIndex', 'statusIndex', 'deviceIndex']:
			if Authentication(params['tip'], user):
				inst_pipe = institutions.objects.get(id = user.inst_id).pipe_id
				options = list(institutions.objects.filter(pipe_id__startswith = inst_pipe).order_by("pipe_id").values_list('pipe_id', 'name', 'is_leaf'))
				code = 0
			return HttpResponse(json.dumps({'data': {'options': options}, 'code': code}))