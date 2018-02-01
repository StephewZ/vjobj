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

from users.models import users, institutions, status_user, status_module, status

def getData(user, opF, pS, cP, sN, oT, mX, sL):
	datas = ''
	pipe_id = institutions.objects.get(id = user.inst_id).pipe_id
	if len(opF) != 0 and pipe_id in opF[-1]:
		opF = opF[-1]
	else:
		opF = pipe_id	

	opF = institutions.objects.filter(pipe_id__startswith = opF).values_list('id')
	data = users.objects.filter(
		Q(nickname__icontains = mX) |
		Q(username__icontains = mX) |
		Q(phone__icontains = mX) |
		Q(address__icontains = mX) |
		Q(remark__icontains = mX),
		is_delete = 0,
		inst_id__in = opF)

	if sN == 'last_login':
		if oT == 'ascending':
			data = data.order_by('last_login')
		elif oT == 'descending':
			data = data.order_by('-last_login')

	total = data.count()
	data = data[(pS*cP-pS):pS*cP]

	ndata = []
	for d in data:
		obj = {}
		obj['nickname'] = d.nickname
		obj['username'] = d.username
		obj['phone'] = d.phone
		obj['address'] = d.address
		obj['inst_name'] = institutions.objects.get(id=d.inst_id).name
		obj['pipe_id'] = institutions.objects.get(id=d.inst_id).pipe_id
		obj['id'] = d.id
		if d.creator != 0:
			obj['creator'] = users.objects.get(id=d.creator).nickname
		else:
			obj['creator'] = ''
			
		status_list = list(status.objects.filter(id__in = status_user.objects.filter(user_id=d.id).values_list( 'status_id')).values('name', 'id'))
		newStatusList = []
		for s in sL + status_list:
			objs = {}
			objs['name'] = s['name']
			objs['id'] = s['id']
			if s in sL:
				objs['disabled'] = False
			else:
				objs['disabled'] = True
			if (objs in newStatusList) == False:
				newStatusList.append(objs)
		obj['statusList'] = newStatusList
		obj['statusName'] =','.join(list(status.objects.filter(id__in = status_user.objects.filter(user_id=d.id).values_list( 'status_id')).values_list('name', flat=True)))
		obj['checkList'] = list(status_user.objects.filter(user_id=d.id).values_list('status_id', flat=True))
		obj['remark'] = d.remark
		if d.last_login != None:
			obj['last_login'] = datetime.strftime(d.last_login, "%Y-%m-%d %H:%M:%S")
		else:
			obj['last_login'] = ''	
		ndata.append(obj)
	datas = {'total': total, 'data': ndata}
	return datas

@login_required
@csrf_exempt
def userList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'userList':
			if Authentication(params['tip'], user):
				code = 0
				pipe_id = institutions.objects.get(id=user.inst_id).pipe_id
				p1 = ''
				plist = []
				for p in pipe_id.split('.'):
					p1 = p1 + p
					plist.append(p1)
				opF = institutions.objects.filter(Q(pipe_id__in = plist) | Q(pipe_id__startswith = pipe_id)).values_list('id')

				pp = institutions.objects.filter(pipe_id__in = plist)
				statusList = list(status.objects.filter(inst_id__in = opF).exclude(~Q(inst_id = user.inst_id), status_type = 0, inst_id__in =pp).values('name', 'id'))

				msg = getData(user, params['optFilters'], params['pageSize'], params['currentPage'], params['sortName'], params['orderType'], params['mixing'], statusList)
			else:
				statusList = []
				msg = 'denied'
				code = 404
			return HttpResponse(json.dumps({'data': {'msg': msg, 'statusList': statusList}, 'code': code}))

@login_required
@csrf_exempt
def userAdd(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'userAdd':
		if Authentication(params['tip'], user):
			code = 0
			err = ''
			username = params['username']
			nickname = params['nickname']
			password1 = params['pass']
			password2 = params['checkPass']
			phone = params['phone']
			address = params['address']
			pipe = params['pipe']
			remark = params['remark']
			if users.objects.filter(username=username).exists():
				code = 2
				err = '添加失败，用户名已存在！'
			elif len(nickname) < 2:
				code = 2
				err = '添加失败，用户昵称最少为 2 位字符！'
			elif len(username) < 4:
				code = 2
				err = '添加失败，用户名最少为 4 位字符！'
			elif len(password1) < 6:
				code = 2
				err = '添加失败，用户密码至少为 6 位字符！'
			elif password1 != password2:
				code = 2
				err = '添加失败，两次输入的密码不一致！'
			elif len(phone) > 20:
				code = 2
				err = '添加失败，联系电话最长为 20 位字符！'
			elif len(address) > 100:
				code = 2
				err = '添加失败，联系地址最长为 100 位字符！'
			elif len(remark) > 100:
				code = 2
				err = '添加失败，描述信息最长为 100 位字符！'
			elif len(pipe) == 0:
				code = 2
				err = '添加失败，请选择用户所属机构'
			elif institutions.objects.filter(pipe_id = pipe[-1]).exists():
				u_pipe = institutions.objects.get(id=user.inst_id).pipe_id
				if u_pipe in pipe[-1]:
					newUser = users.objects.create_user(creator=user.id,username=username, nickname=nickname, 
						password=password1, phone=phone, address=address, remark=remark, inst_id=institutions.objects.get(pipe_id=pipe[-1]).id)
					for s in params['checkList']:
						status_user.objects.create(user_id=newUser.id,status_id=s)
			else:
				code = 2
				err = '发生未知错误，请刷新页面重试！'
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code, 'err': err}))

@login_required
@csrf_exempt
def userDel(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'userDel':
		if Authentication(params['tip'], user):
			code = 0
			i = 0
			j = 0
			for d in params['delList']:
				if int(d['id']) == user.id:
					code = 2
					i = i + 1
				elif institutions.objects.get(id=user.inst_id).pipe_id in institutions.objects.get(id=users.objects.get(id=d['id']).inst_id).pipe_id:
					users.objects.filter(id=d['id']).update(is_delete=1, nickname = '')
					status_user.objects.filter(user_id=d['id']).delete()
					j = j + 1
				else:
					i = i + 1	
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'err': i, 'err_ok': j}, 'code': code}))

@login_required
@csrf_exempt
def userEdit(request):
	code = 1
	msg = ''
	user =request.user
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'userEdit':
		if Authentication(params['tip'], user):
			code = 0
			users.objects.filter(username=params['username'], id = params['id']).update(nickname=params['nickname'],phone=params['phone'],
				address=params['address'],inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id, remark=params['remark'])
			sList = list(status_user.objects.filter(user_id=params['id']).values_list('status_id', flat = True))

			for s in params['checkList']:
				if s in sList:
					continue
				else:	
					status_user.objects.create(user_id = params['id'], status_id = s, creator=user.id)
			for ss in sList:
				if ss in params['checkList']:
					continue
				else:
					status_user.objects.filter(status_id = ss).delete()			
		else:
			msg = 'denied'
			code = 404		
	return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))