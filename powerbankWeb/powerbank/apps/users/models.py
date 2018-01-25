#-*-encoding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class users(AbstractUser):
	inst_id = models.IntegerField(default=0) #所属机构id
	nickname = models.CharField(max_length=50, default='')
	phone = models.CharField(max_length=16, null=True, blank=True)
	address = models.CharField(max_length=100, default='')
	is_delete = models.BooleanField(default=False)
	user_type = models.IntegerField(default=0)
	remark = models.CharField(max_length=255, default='')
	class Meta:
		db_table='users'

	def __unicode__(self):
		return self.username

class accounts(models.Model):
	user_id = models.IntegerField(null=True, blank=True)
	wechat_openId = models.CharField(max_length=28, null=True, blank=True)
	wechat_merchant = models.CharField(max_length=32, null=True, blank=True)
	wechat_appId = models.CharField(max_length=32, null=True, blank=True)
	wechat_appSecret = models.CharField(max_length=32, null=True, blank=True)
	wechat_apiSecret = models.CharField(max_length=64, null=True, blank=True)
	wechat_certificate = models.CharField(max_length=64, null=True, blank=True)
	wechat_certificate_password = models.CharField(max_length=64, null=True, blank=True)
	wechat_personalAccount = models.CharField(max_length=64, null=True, blank=True)
	wechat_personalName = models.CharField(max_length=128, null=True, blank=True)
	wechat_rate = models.IntegerField(default=100)
	alipay_appId = models.CharField(max_length=32, null=True, blank=True)
	alipay_privateKey = models.CharField(max_length=4096, null=True, blank=True)
	alipay_publicKey = models.CharField(max_length=4096, null=True, blank=True)
	alipay_sellerId = models.CharField(max_length=28, null=True, blank=True)
	alipay_productCode = models.CharField(max_length=64, null=True, blank=True)
	alipay_personalAccount = models.CharField(max_length=64, null=True, blank=True)
	alipay_personalName = models.CharField(max_length=128, null=True, blank=True)
	alipay_rate = models.IntegerField(default=100)
	hotline = models.CharField(max_length=64, null=True, blank=True)
	qrcode = models.CharField(max_length=256, null=True, blank=True)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='accounts'

class institutions(models.Model): #机构表
	pipe_id = models.CharField(max_length=255,default = '') #管道id
	parent_id = models.IntegerField(null=True, blank=True) #父节点id
	is_leaf = models.BooleanField(default=True) #节点末端判断
	inst_type = models.CharField(max_length=255,default = '') #机构类型
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
	status_type = models.IntegerField(null=True, blank=True) #角色类型
	is_enabled = models.BooleanField(default=True) #是否启用
	creator = models.IntegerField(null=True, blank=True) #创建用户id user_id
	create_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='')

	class Meta:
		db_table='status'

class funcmodule(models.Model): #功能模块表
	pipe_id = models.CharField(max_length=255,default = '') #管道id
	parent_id = models.IntegerField(null=True, blank=True) #父节点id
	name = models.CharField(max_length=50, default='') #功能模块名称
	url = models.CharField(max_length=255,default = '')
	is_leaf = models.CharField(max_length=255,default = '')
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
	device_num = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=48, default='')
	user_id = models.IntegerField(null=True, blank=True)
	creator = models.IntegerField(default=1)
	create_time = models.DateTimeField(default=datetime.now)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='devices'

class operation_note(models.Model):
	user_id = models.IntegerField(null=True, blank=True)
	operate_time = models.DateTimeField(null=True, blank=True)
	operate_type = models.CharField(max_length=2048, default='')
	old_data = models.CharField(max_length=2048, default='')
	new_data = models.CharField(max_length=2048, default='')
	remark = models.CharField(max_length=2048, default='') #备注

	class Meta:
		db_table='operation_note'
