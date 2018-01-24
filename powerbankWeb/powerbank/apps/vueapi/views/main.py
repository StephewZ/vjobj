# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import json

from users.models import users, institutions, status_user, status_module

@login_required
def main_view(request):
	return render(request, 'index.html')

@login_required
@csrf_exempt
def index(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		options = ''
		code = 1
		if params['tip'] in ['instIndex', 'userIndex']:
			status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
			if status_module.objects.filter(status_id__in = status_id_list, module_id = 3).exists():
				inst_pipe = institutions.objects.get(id = user.inst_id).pipe_id
				options = list(institutions.objects.filter(pipe_id__startswith = inst_pipe).order_by("pipe_id").values_list('pipe_id', 'name', 'is_leaf'))
				code = 0
	return HttpResponse(json.dumps({'data': {'options': options}, 'code': code}))