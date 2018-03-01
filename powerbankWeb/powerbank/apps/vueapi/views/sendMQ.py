#!/usr/bin/env python
#coding=utf8
import pika
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json
import random

from users.models import devices, goods, goods_pipe, goods_pipe_device

MQ_IP = 'test1.amqp.gzncloud.com'
MQ_PORT = 5672
MQ_ID = 'ssdd01'
MQ_PW = '*ssdd_password#'
MQ_exchange = 'to_ssdd_server'

limit = 255

line = [5, 7, 11, 13]

times = [51, 36, 23, 19]

def sendMQ_(key, body):
	credentials = pika.PlainCredentials(MQ_ID, MQ_PW)

	connection = pika.BlockingConnection(pika.ConnectionParameters(
	               MQ_IP, MQ_PORT, '/', credentials))
	channel = connection.channel()
	 
	channel.basic_publish(exchange=MQ_exchange, routing_key=key, body=body)
	print (" [x] Sent: " + " routing_key=" + key + " body=" + body)
	connection.close()

def tenTofour(x):
	lists = []
	while  x > 3:
		lists.append(str(x%4))
		x = x // 4
	if x:
		lists.append(str(x))
	x = ''.join(reversed(lists))	
	return x

@csrf_exempt
def sendMQ(request):
	params = json.loads(request.body.decode())['params']['tips']
	device = params['device']
	sequence = params['sequence']
	# device_id = devices.objects.get(device_num=device).id
	# goods_pipe_id = goods_pipe_device.objects.get(device_id=device_id, sequence=sequence)
	device_type = devices.objects.get(device_num=device).device_type
	if device_type == 1:
		remark = goods_pipe.objects.get(id=goods_pipe_device.objects.get(device_id=devices.objects.get(device_num=device).id, sequence=sequence-1).goods_pipe_id).remark
		if u'热饮' in remark:
			ttype = 1
		else:
			ttype = 0
		msga = 'operation:' + str(device)
		msgb = [int(sequence), 1, ttype, 0,0,0,0,0]
		msgb = str(bytes(msgb), encoding='utf-8')
		sendMQ_(msga, msgb)
	elif device_type == 2:
		sequence = ''
		gs = random.randint(0, 4)
		gs_line = line[gs]
		goal = random.randint(1, times[gs])
		goal = tenTofour(goal*gs_line)
		sequence = int(str(gs) + goal) + 1111
	return HttpResponse(json.dumps({'data': {'device': device, 'sequence': sequence}}))

