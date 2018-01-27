# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

import json
from datetime import datetime

from users.models import users, institutions, status_user, status_module

@login_required
@csrf_exempt
def userList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'userList':
			return

@login_required
@csrf_exempt
def userAdd(request):
	return

@login_required
@csrf_exempt
def userDel(request):
	return		

@login_required
@csrf_exempt
def userEdit(request):
	return