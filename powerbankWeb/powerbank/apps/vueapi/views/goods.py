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

from users.models import users, institutions, status_user, status_module, goods, goods_pipe


def getData(user, opF, pS, cP, sN, oT, mX):
	pipe_id = institutions.objects.get(id = user.inst_id).pipe_id
	if len(opF) != 0 and pipe_id in opF[-1]:
		opF = opF[-1]
		opF = institutions.objects.filter(pipe_id = opF).values_list('id')
	else:
		opF = pipe_id
		opF = institutions.objects.filter(pipe_id__startswith = opF).values_list('id')
	data = goods.objects.filter(
		Q(name__icontains = mX) |
		Q(goods_num__icontains = mX) |
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
	elif sN == 'purchase_price':
		if oT == 'ascending':
			data = data.order_by('purchase_price')
		elif oT == 'descending':
			data = data.order_by('-purchase_price')
	elif sN == 'retail_price':
		if oT == 'ascending':
			data = data.order_by('retail_price')
		elif oT == 'descending':
			data = data.order_by('-retail_price')	

	total = data.count()
	data = data[(pS*cP-pS):pS*cP]

	ndata = []
	for d in data:
		obj = {}
		obj['goods_num'] = d.goods_num
		obj['name'] = d.name
		obj['parent'] = institutions.objects.get(id = d.inst_id).name
		obj['pipe_id'] = institutions.objects.get(id=d.inst_id).pipe_id
		obj['id'] = d.id
		obj['creator'] = users.objects.get(id=d.creator).nickname
		obj['remark'] = d.remark
		p_price = str(d.purchase_price/100)
		r_price = str(d.retail_price/100)
		if p_price.split('.')[1] == '0':
			obj['purchase_price'] = p_price[0]
		else:
			obj['purchase_price'] = p_price

		if r_price.split('.')[1] == '0':
			obj['retail_price'] = r_price[0]
		else:
			obj['retail_price'] = r_price 
		obj['currency'] = d.currency
		obj['made_time'] = datetime.strftime(d.create_time, "%Y-%m-%d %H:%M:%S")
		obj['edit_time'] = datetime.strftime(d.edit_time, "%Y-%m-%d %H:%M:%S")
		ndata.append(obj)
	datas = {'total': total, 'data': ndata}
	return datas

@login_required
@csrf_exempt
def goodsList(request):
	if request.method == "POST":
		user = request.user
		params = json.loads(request.body.decode())['params']['tips']
		code = 1
		if params['tip'] == 'goodsList':
			if Authentication(params['tip'], user):
				code = 0
				msg = getData(user, params['optFilters'], params['pageSize'], params['currentPage'], params['sortName'], params['orderType'], params['mixing'])
			else:
				msg = 'denied'
				code = 404
			return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def goodsAdd(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'goodsAdd':
		if Authentication(params['tip'], user):
			code = 0
			if goods.objects.filter(goods_num=params['goods_num'], inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id).exists() == False:
				goods.objects.create(goods_num=params['goods_num'],name=params['name'],remark=params['remark'],
					inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id,creator=user.id, purchase_price=params['p_price'], retail_price=params['r_price'])
			elif goods.objects.filter(goods_num=params['goods_num'], inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id).exists():
				code = 2
			else:
				code = 3
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))

@login_required
@csrf_exempt
def goodsDel(request):
	user = request.user
	msg = ''
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'goodsDel':
		if Authentication(params['tip'], user):
			code = 0
			i = 0
			j = 0
			for d in params['delList']:
				if goods.objects.filter(goods_num=d['goods_num'], id=d['id']).exists():
					if goods_pipe.objects.filter(goods_id=d['id']).exists() == False:
						j = j + 1
						goods.objects.filter(goods_num=d['goods_num'], id=d['id']).delete()
					else:
						code = 2
						i = i + 1	
				else:
					code = 2
					i= i + 1	
		else:
			msg = 'denied'
			code = 404
		return HttpResponse(json.dumps({'data': {'err': i, 'err_ok': j}, 'code': code}))

@login_required
@csrf_exempt
def goodsEdit(request):
	code = 1
	msg = ''
	user =request.user
	params = json.loads(request.body.decode())['params']['tips']
	if params['tip'] == 'goodsEdit':
		if Authentication(params['tip'], user):
			code = 0
			if goods.objects.filter(goods_num=params['goods_num'], inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id).exclude(id=params['id']).exists() == False:
				goods.objects.filter(id = params['id']).update(goods_num=params['goods_num'], 
					name=params['name'],inst_id=institutions.objects.get(pipe_id=params['pipe'][-1]).id, purchase_price = params['p_price'], retail_price = params['r_price'],
					remark=params['remark'], edit_time = datetime.now())
			else:
				code = 2
		else:
			msg = 'denied'
			code = 404		
	return HttpResponse(json.dumps({'data': {'msg': msg}, 'code': code}))	