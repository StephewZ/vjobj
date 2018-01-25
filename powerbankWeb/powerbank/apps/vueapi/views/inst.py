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
			data = data.order_by('edit_time')
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
		obj['remark'] = d.remark
		obj['is_leaf'] = d.is_leaf
		ndata.append(obj)
	datas = {'total': total, 'data': ndata}
	return datas

def get0(num):
	while len(num) < 3:
		num = '0' + num
	return num	
			

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

@login_required
@csrf_exempt
def instAdd(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'instAdd':
			status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
			if status_module.objects.filter(status_id__in = status_id_list, module_id = 3).exists():
				p_pipe_id = params['pipe'][-1]
				u_id = institutions.objects.get(id=user.inst_id).pipe_id

				if u_id in p_pipe_id and p_pipe_id != u_id:
					p_id = institutions.objects.get(pipe_id=p_pipe_id).id

					if institutions.objects.filter(parent_id=p_id).exists():
						newp_id = institutions.objects.filter(parent_id=p_id).order_by('-pipe_id')[0].pipe_id
						newp_id2 = get0(str(int(newp_id.split('.')[-1]) + 1))
						newp_id = newp_id[:-3] + newp_id2
						institutions.objects.create(name=params['name'], remark=params['remark'], parent_id=p_id, is_leaf=True, pipe_id=newp_id, creator= user.id)
					else:
						institutions.objects.filter(pipe_id=p_pipe_id).update(is_leaf=False)
						newp_id = p_pipe_id + '.001'
						institutions.objects.create(name=params['name'], remark=params['remark'], parent_id=p_id, is_leaf=True, pipe_id=newp_id, creator= user.id)
					code = 0
		return HttpResponse(json.dumps({'data': {'msg': 'ok'}, 'code': code}))

def delRule(pipe):

	return

@login_required
@csrf_exempt
def instDel(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'instDel':
			status_id_list = status_user.objects.filter(user_id = user.id).values_list('status_id')
			if status_module.objects.filter(status_id__in = status_id_list, module_id = 3).exists():
				code = 0
				for d in params['delList']:
					if institutions.objects.get(pipe_id=d['pipe_id']).is_leaf == False:
						code =2
					else:
						bro_inst = institutions.objects.filter(pipe_id__gt = d['pipe_id'], pipe_id__in = (d['pipe_id'], d['pipe_id'][:-3] + '999'))
						print(bro_inst)
						if len(bro_inst) != 0:
							institutions.objects.filter(pipe_id=d['pipe_id']).delete()
							bro_inst.update(pipe_id = F('pipe_id')[:-3] + get0(str(int(F('pipe_id').split('.')[-1]) + 1)))
						else:
							institutions.objects.filter(pipe_id=d['pipe_id']).delete()
						return HttpResponse(json.dumps({'data': {'msg': 'ok'}, 'code': code}))
