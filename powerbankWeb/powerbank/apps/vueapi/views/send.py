#!/usr/bin/env python
#coding=utf8
import pika
from django.views.decorators.csrf import csrf_exempt

from users.models import devices, goods, goods_pipe, goods_pipe_device

@csrf_exempt
def sendMQ(request):
	params = json.loads(request.body.decode())['params']['tips']
	device = params['device']
	sequence = params['sequence']

	remark = goods_pipe(id=goods_pipe_device(device_id=devices.objects.get(device_num=device), sequence=sequence).goods_pipe_id).remark

	if u'热饮' in remark:
		remark = 1
	else:
		remark = 0	
	MQ_IP = 'test1.amqp.gzncloud.com'
	MQ_PORT = 5672
	MQ_ID = 'ssdd01'
	MQ_PW = '*ssdd_password#'
	MQ_exchange = 'to_ssdd_server'

	def sentMQ(key, body):
		credentials = pika.PlainCredentials(MQ_ID, MQ_PW)

		connection = pika.BlockingConnection(pika.ConnectionParameters(
		               MQ_IP, MQ_PORT, '/', credentials))
		channel = connection.channel()
		 
		channel.basic_publish(exchange=MQ_exchange, routing_key=key, body=body)
		print (" [x] Sent: " + " routing_key=" + key + " body=" + body)
		connection.close()
	msga = 'operation' + str(device)
	msgb = [int(sequence),1,remark,0,0,0,0,0]
	msgb = str(bytes(msgb))
	sentMQ(msga, msgb)