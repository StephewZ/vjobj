# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F,Q

from .permit import Authentication

import json
from datetime import datetime

from users.models import users, institutions, status_user, status_module, status, funcmodule

def getData(user, opF, pS, cP, sN, oT):
	pipe_id = institutions.objects.get(id = user.inst_id).pipe_id
	if len(opF) != 0 and pipe_id in opF[-1]:
		opF = opF[-1]
	else:
		opF = pipe_id
	p1 = ''
	plist = []
	for p in opF.split('.'):
		p1 = p1 + p
		plist.append(p1)
	opF = institutions.objects.filter(Q(pipe_id__in = plist) | Q(pipe_id__startswith = pipe_id)).values_list('id')
	
	pp = institutions.objects.filter(pipe_id__in = plist)
	data = status.objects.filter(inst_id__in = opF).exclude(~Q(inst_id = user.inst_id), status_type = 0, inst_id__in =pp)

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
		obj['name'] = d.name
		obj['id'] = d.id
		obj['parent'] = institutions.objects.get(id = d.inst_id).name
		if d.is_enabled == True:
			obj['is_enabled'] = '启用'
		else:
			obj['is_enabled'] = '禁用'
		obj['status_type'] = d.status_type
		obj['creator'] = users.objects.get(id = d.creator).nickname
		obj['made_time'] = datetime.strftime(d.create_time, "%Y-%m-%d %H:%M:%S")
		obj['edit_time'] = datetime.strftime(d.edit_time, "%Y-%m-%d %H:%M:%S")
		obj['remark'] = d.remark
		modulelist = list(funcmodule.objects.filter(id__in = status_module.objects.filter(status_id = d.id).values_list('module_id')).order_by('pipe_id').values_list('pipe_id', flat=True))
		obj['powerlist'] = modulelist
		ndata.append(obj)
	datas = {'total': total, 'data': ndata}
	return datas

@login_required
@csrf_exempt
def statusList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'statusList':
			if Authentication(params['tip'], user):
				code = 0
				msg = getData(user, params['optFilters'], params['pageSize'], params['currentPage'], params['sortName'], params['orderType'])
				plist = list(funcmodule.objects.all().order_by('pipe_id').values_list('pipe_id', 'name', 'is_leaf'))
				suList = status_user.objects.filter(user_id= user.id).values_list('status_id')
				smList = status_module.objects.filter(status_id__in = suList).values_list('module_id')
				permitList = list(funcmodule.objects.filter(id__in = smList).order_by('pipe_id').values_list('pipe_id', flat=True))
			else:
				plist = []
				permitList = []
				msg = 'denied'
				code = 404
			return HttpResponse(json.dumps({'data': {'msg': msg, 'plist': plist, 'permitList': permitList}, 'code': code}))

@login_required
@csrf_exempt
def statusAdd(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'statusAdd':
		if Authentication(params['tip'], user):
			code = 0
			err = ''
			if params['is_enabled'] == '启用':
				is_enabled = 1
			else:
				is_enabled = 0
			newStatus = status.objects.create(name=params['name'], status_type=params['status_type'],is_enabled=is_enabled, creator = user.id, inst_id=user.inst_id)
			plist = list(funcmodule.objects.all().order_by('pipe_id').values_list('pipe_id', flat=True))
			smList = []
			for p in params['powers']:
				# if (funcmodule.objects.get(pipe_id=p).id)
				newStatus_module = status_module(status_id = newStatus.id, module_id=funcmodule.objects.get(pipe_id=p).id, auth_type=1,creator=user.id)
				smList.append(newStatus_module)
			status_module.objects.bulk_create(smList)
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
	if params['tip'] == 'statusDel':
		if Authentication(params['tip'], user):
			code = 0
			for dels in params['delList']:
				status.objects.filter(id=dels['id']).delete()
				status_module.objects.filter(status_id=dels['id']).delete()
				status_user.objects.filter(status_id=dels['id']).delete()
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def statusEdit(request):
	user = request.user
	code = 1
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'statusEdit':
		if Authentication(params['tip'], user):
			code = 0
			err = ''
			if params['is_enabled'] == '启用':
				is_enabled = 1
			else:
				is_enabled = 0
			status.objects.filter(id=params['id']).update(name=params['name'],status_type=params['status_type'],is_enabled=is_enabled)
			status_module.objects.filter(status_id=params['id']).delete()
			smList = []
			for p in params['powers']:
				newStatus_module = status_module(status_id = params['id'], module_id=funcmodule.objects.get(pipe_id=p).id, auth_type=1,creator=user.id)
				smList.append(newStatus_module)
			status_module.objects.bulk_create(smList)
		else:
			msg = 'denied'
			code = 404	
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))