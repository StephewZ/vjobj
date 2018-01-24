# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import datetime

from users.models import users, institutions, status_user, status_module

def getData(user, opF, pS, cP, sN, oT):
	if len(opF) != 0:
		opF = opF[-1]
	else:
		opF = institutions.objects.get(id = user.inst_id).pipe_id

	data = institutions.objects.filter(pipe_id__startswith = opF).exclude(id = user.inst_id)
	
	if sN == 'made_time':
		if oT == 'ascending':
			data = data.order_by('create_time')
		elif oT == 'descending':
			data = data.order_by('-create_time')
	elif sN == 'edit_time':
		if oT == 'ascending':
			data = data.order_by('-edit_time')
		elif oT == 'descending':
			data = data.order_by('-edit_time')
	total = len(data)
	data = data[(pS*cP-pS):pS*cP]

	ndata = []
	for d in data:
		obj = {}
		obj['name'] = d.name
		if d.parent_id != 0 and d.parent_id != 1:
			obj['parent'] = institutions.objects.get(id = d.parent_id).name
		else:
			obj['parent'] = ''	
		obj['creator'] = users.objects.get(id = d.creator).nickname
		obj['made_time'] = datetime.strftime(d.create_time, "%Y-%m-%d %H:%M:%S")
		obj['edit_time'] = datetime.strftime(d.edit_time, "%Y-%m-%d %H:%M:%S")
		obj['pipe_id'] = d.pipe_id
		ndata.append(obj)
	datas = {'total': total, 'data': ndata}
	return datas

@login_required
@csrf_exempt
def instList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'instList':
			status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
			if status_module.objects.filter(status_id__in = status_id_list, module_id = 3).exists():
				msg = getData(user, params['optFilters'], params['pageSize'], params['currentPage'], params['sortName'], params['orderType'])
				code = 0
	return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))