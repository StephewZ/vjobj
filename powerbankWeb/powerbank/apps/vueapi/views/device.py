# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .permit import Authentication

import json
from datetime import datetime

from users.models import users, institutions, status_user, status_module, devices

from ..models import device_inst

def getData(user, opF, pS, cP, sN, oT, mX):
	pipe_id = institutions.objects.get(id = user.inst_id).pipe_id
	if len(opF) != 0 and pipe_id in opF[-1]:
		opF = opF[-1]
		opF = institutions.objects.filter(pipe_id = opF).values_list('id')
	else:
		opF = pipe_id
		opF = institutions.objects.filter(pipe_id__startswith = opF).values_list('id')
	data = devices.objects.filter(
		Q(name__icontains = mX) |
		Q(device_num__icontains = mX) |
		Q(remark__icontains = mX),
		inst_id__in = opF)
	if Authentication('admin', user) == False:
		data = data.exclude(status = 0)
	if sN == 'made_time':
		if oT == 'ascending':
			data = data.order_by('create_time')
		elif oT == 'descending':
			data = data.order_by('-create_time')
	elif sN == 'edit_time':
		if oT == 'ascending':
			data = data.order_by('edit_time')
		elif oT == 'descending':
			data = data.order_by('-edit_time')

	total = data.count()
	data = data[(pS*cP-pS):pS*cP]

	ndata = []
	for d in data:
		obj = {}
		obj['device_num'] = d.device_num
		obj['name'] = d.name
		obj['parent'] = institutions.objects.get(id = d.inst_id).name
		obj['pipe_id'] = institutions.objects.get(id=d.inst_id).pipe_id
		obj['id'] = d.id
		obj['creator'] = users.objects.get(id=d.creator).nickname
		obj['remark'] = d.remark
		obj['made_time'] = datetime.strftime(d.create_time, "%Y-%m-%d %H:%M:%S")
		obj['edit_time'] = datetime.strftime(d.edit_time, "%Y-%m-%d %H:%M:%S")
		ndata.append(obj)
	datas = {'total': total, 'data': ndata}
	return datas

@login_required
@csrf_exempt
def deviceList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'deviceList':
			if Authentication(params['tip'], user):
				code = 0
				msg = getData(user, params['optFilters'], params['pageSize'], params['currentPage'], params['sortName'], params['orderType'], params['mixing'])
			else:
				msg = 'denied'
				code = 404
			return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def deviceAdd(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'deviceAdd':
		if Authentication(params['tip'], user):
			code = 0
			if devices.objects.filter(device_num=params['device_num'], status=0).exists():
				now = datetime.now()
				devices.objects.filter(device_num=params['device_num'], id=params['id']).update(name=params['name'],remark=params['remark'],
					inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id,creator=user.id, status = 1,edit_time=now,create_time=now)
			elif devices.objects.filter(device_num=params['device_num']).exists() == False and Authentication('admin', user):
				devices.objects.create(device_num=params['device_num'],name=params['name'],remark=params['remark'],
					inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id,creator=user.id, status = 0)
			elif devices.objects.filter(device_num=params['device_num']).exists():
				code = 2
			else:
				code = 3
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def deviceDel(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'deviceDel':
		if Authentication(params['tip'], user):
			code = 0
			i = 0
			j = 0
			for d in params['delList']:
				if devices.objects.filter(device_num=d['device_num'], id=d['id'], status=1).exists():
					j = j + 1
					devices.objects.filter(device_num=d['device_num'], id=d['id']).update(status=0, name='', remark='', edit_time = datetime.now())
				elif devices.objects.filter(device_num=d['device_num'], id=d['id'], status=0).exists() and Authentication('admin', user):
					j = j + 1
					devices.objects.filter(device_num=d['device_num'], id=d['id'], status=0).delete()
				else:
					code = 2
					i= i + 1	
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'err': i, 'err_ok': j}, 'code': code}))

@login_required
@csrf_exempt
def deviceEdit(request):
	code = 1
	msg = ''
	user =request.user
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'deviceEdit':
		if Authentication(params['tip'], user):
			code = 0
			devices.objects.filter(device_num=params['device_num'], id = params['id']).update(name=params['name'],inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id,
				remark=params['remark'], edit_time = datetime.now())
		else:
			msg = 'denied'
			code = 404		
	return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))	