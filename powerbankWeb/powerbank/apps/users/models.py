#-*-encoding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class users(AbstractUser):
	inst_id = models.IntegerField(default=0) #所属机构id
	nickname = models.CharField(max_length=50, default='')
	creator = models.IntegerField(default=0)
	phone = models.CharField(max_length=16, null=True, blank=True)
	address = models.CharField(max_length=100, default='')
	is_delete = models.BooleanField(default=False)
	user_type = models.IntegerField(default=0)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='')
	class Meta:
		db_table='users'

	def __unicode__(self):
		return self.username

class accounts(models.Model):
	user_id = models.IntegerField(null=True, blank=True) #所属用户
	wechat_merchant = models.CharField(max_length=32, null=True, blank=True) #微信商户号
	wechat_appId = models.CharField(max_length=32, null=True, blank=True) #微信应用号
	wechat_appSecret = models.CharField(max_length=32, null=True, blank=True) #微信引用密钥
	wechat_apiSecret = models.CharField(max_length=64, null=True, blank=True)  #微信api密钥
	wechat_certificate = models.CharField(max_length=64, null=True, blank=True) #微信证书 文件名
	wechat_certificate_password = models.CharField(max_length=64, null=True, blank=True) #微信api证书(.p12文件) 密码
	wechat_personalAccount = models.CharField(max_length=64, null=True, blank=True) #微信个人收款账号
	wechat_personalName = models.CharField(max_length=128, null=True, blank=True) #微信个人账号名称
	wechat_auxiliaryRate = models.IntegerField(default=5) #微信提现手续费
	wechat_rate = models.IntegerField(default=100) #微信折扣
	alipay_appId = models.CharField(max_length=32, null=True, blank=True) #支付宝商户appid
	alipay_privateKey = models.CharField(max_length=4096, null=True, blank=True) #支付宝应用私钥(PKCS8格式)
	alipay_publicKey = models.CharField(max_length=4096, null=True, blank=True) #支付宝公钥
	alipay_sellerId = models.CharField(max_length=28, null=True, blank=True) #收款支付宝用户ID
	alipay_productCode = models.CharField(max_length=64, null=True, blank=True) #商家和支付宝签约的产品码
	alipay_personalAccount = models.CharField(max_length=64, null=True, blank=True) #支付宝个人收款账号
	alipay_personalName = models.CharField(max_length=128, null=True, blank=True) #支付宝个人收款账号名称
	alipay_auxiliaryRate = models.IntegerField(default=5) #支付宝提现手续费
	alipay_rate = models.IntegerField(default=100) #支付宝折扣
	hotline = models.CharField(max_length=64, null=True, blank=True) #客服电话
	qrcode = models.CharField(max_length=256, null=True, blank=True) #客服二维码
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='accounts'

class institutions(models.Model): #机构表
	pipe_id = models.CharField(max_length=255,default = '') #管道id
	parent_id = models.IntegerField(null=True, blank=True) #父节点id
	is_leaf = models.BooleanField(default=True) #节点末端判断
	inst_type = models.CharField(max_length=255,default = 1) #机构类型
	name = models.CharField(max_length=50, default='') #机构名称
	creator = models.IntegerField(null=True, blank=True) #创建用户id user_id
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	is_delete = models.BooleanField(default=False)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='institutions'

class status(models.Model): #角色表
	name = models.CharField(max_length=28, default='')
	inst_id = models.IntegerField(default=0) #所属机构id
	status_type = models.IntegerField(default=1) #角色类型
	is_enabled = models.BooleanField(default=True) #是否启用
	creator = models.IntegerField(null=True, blank=True) #创建用户id user_id
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='')

	class Meta:
		db_table='status'

class funcmodule(models.Model): #功能模块表
	pipe_id = models.CharField(max_length=255,default = '') #管道id
	parent_id = models.IntegerField(null=True, blank=True) #父节点id
	name = models.CharField(max_length=50, default='') #功能模块名称
	url = models.CharField(max_length=255,default = '')
	is_leaf = models.BooleanField(default=True) #节点末端判断
	is_enabled = models.BooleanField(default=True)
	sort_num = models.IntegerField(null=True, blank=True)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='funcmodule'

class status_user(models.Model):
	status_id = models.IntegerField(null=True, blank=True)
	user_id = models.IntegerField(null=True, blank=True)
	creator = models.IntegerField(null=True, blank=True)
	create_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table = 'status_user'

class status_module(models.Model): #角色 功能模块 关联表
	status_id = models.IntegerField(null=True, blank=True)
	module_id = models.IntegerField(null=True, blank=True)
	auth_type = models.IntegerField(null=True, blank=True)
	creator = models.IntegerField(null=True, blank=True)
	create_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='status_module'

class devices(models.Model):
	device_num = models.IntegerField(null=True, blank=True)
	inst_id = models.IntegerField(null=True, blank=True)
	user_id = models.IntegerField(null=True, blank=True)
	status = models.IntegerField(default=0)
	name = models.CharField(max_length=48, default='')
	creator = models.IntegerField(default=1)
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='devices'

class operation_note(models.Model):
	user_id = models.IntegerField(null=True, blank=True)
	operate_time = models.DateTimeField(null=True, blank=True)
	operate_type = models.CharField(max_length=2048, default='')
	old_data = models.CharField(max_length=2048, default='')
	new_data = models.CharField(max_length=2048, default='')
	create_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=2048, default='') #备注

	class Meta:
		db_table='operation_note'

class orders(models.Model):
	trade_no = models.CharField(max_length=32, default='') #本地唯一编号 订单号
	platform_trade_no = models.CharField(max_length=64, default='') #支付平台订单号
	refund_trade_no = models.CharField(max_length=32, null=True, blank=True) #退款订单号
	refund_platform_trade_no = models.CharField(max_length=64, null=True, blank=True) #支付平台退款订单号
	merchant_no = models.CharField(max_length=32, default='') #微信商户号/支付宝收款账号
	created_at = models.DateTimeField(default=datetime.now) #订单创建时间
	payed_at = models.DateTimeField(null=True, blank=True) #支付完成时间
	refunded_at = models.DateTimeField(null=True, blank=True) #发起退款时间
	payed = models.BooleanField(default=False) #是否支付成功
	communication_succeeded = models.BooleanField(default=False) #请求设备操作是否成功
	refunded = models.BooleanField(default=False) #退款是否成功
	order_tpye = models.BooleanField(default=False) #订单类型
	customer1 = models.CharField(max_length=32, default='') #客户信息1
	customer2 = models.CharField(max_length=256, default='') #客户信息2
	device = models.IntegerField(null=True, blank=True) #所属设备
	user = models.IntegerField(null=True, blank=True) #收款用户
	payment_channel = models.CharField(max_length=32, default='') #支付方式
	initial_amount = models.IntegerField(null=True, blank=True) #应付金额
	rate = models.IntegerField(default=100) #折扣
	discounted_amount = models.IntegerField(null=True, blank=True) #折后金额
	currency = models.CharField(max_length=30, default='CNY') #币种
	remark = models.CharField(max_length=256, null=True,blank=True) #备注

	class Meta:
		db_table='orders'

class withdrawals(models.Model):
	trade_no = models.CharField(max_length=32, default='') #本地唯一编号
	platform_trade_no = models.CharField(max_length=64, default='') #支付平台订单号
	user_id = models.IntegerField(null=True, blank=True) #收款用户
	payment_channel = models.CharField(max_length=32, default='') #支付方式
	amount = models.IntegerField(null=True, blank=True) #金额(分)
	auxiliary = models.IntegerField(null=True, blank=True) #手续费(分)
	account = models.CharField(max_length=256, default='') #收款账号
	account_name = models.CharField(max_length=256, default='') #收款账号名称
	period_from = models.DateTimeField(default=datetime.now) #提现周期起始时间
	period_to = models.DateTimeField(default=datetime.now) #提现周期结束时间
	succeeded = models.IntegerField(null=True, blank=True) #是否成功 默认NULL宝石未知
	timestamp = models.DateTimeField(default=datetime.now) #操作时间
	remark = models.CharField(max_length=256, null=True,blank=True) #备注

	class Meta:
		db_table='withdrawals'

class goods_pipe(models.Model):
	goods_pipe_num = models.CharField(max_length=28, default='')
	goods_id = models.IntegerField(default=0)
	name = models.CharField(max_length=28, default='')
	currency = models.CharField(max_length=30, default='CNY')
	purchase_price = models.IntegerField(null=True, blank=True) #成本
	retail_price = models.IntegerField(null=True, blank=True) #售价
	goods_pipe_type = models.IntegerField(default=1) #类型
	creator = models.IntegerField(null=True, blank=True) #创建用户id user_id
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='')

	class Meta:
		db_table='goods_pipe'

class goods_pipe_device(models.Model):
	goods_pipe_id = models.IntegerField(default=0)
	device_id = models.IntegerField(default=0)
	sequence = models.IntegerField(default=1)
	creator = models.IntegerField(null=True, blank=True) #创建用户id user_id
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='')

	class Meta:
		db_table='goods_pipe_device'

class goods(models.Model):
	goods_num = models.CharField(max_length=28, default='')
	name = models.CharField(max_length=28, default='')
	inst_id = models.IntegerField(default=0) #所属机构id
	purchase_price = models.IntegerField(null=True, blank=True) #成本
	retail_price = models.IntegerField(null=True, blank=True) #售价
	currency = models.CharField(max_length=30, default='CNY')
	goods_type = models.IntegerField(default=1) #商品类型
	creator = models.IntegerField(null=True, blank=True) #创建用户id user_id
	create_time = models.DateTimeField(default=datetime.now)
	edit_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='')

	class Meta:
		db_table='goods'