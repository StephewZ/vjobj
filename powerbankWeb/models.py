#-*-encoding:utf-8 -*-
from datetime import datetime

from django.db import models

from users.models import users

from time import strftime
from datetime import datetime
# Create your models here.


class teams(models.Model):
	team = models.AutoField(primary_key=True)
	user = models.ForeignKey(users, blank=True, null=True, on_delete=models.SET_NULL,db_column='user')
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=256, null=True, blank=True)
	created_at = models.DateTimeField(default=datetime.now)
	class Meta:
         db_table='teams'

class devices(models.Model):
	user = models.ForeignKey(users, blank=True, null=True, on_delete=models.SET_NULL,db_column='user')
	device = models.IntegerField(primary_key=True)
	payee = models.IntegerField(default=0)
	team = models.ForeignKey(teams, blank=True, null=True, on_delete=models.SET_NULL,db_column='team')
	status = models.CharField(max_length=32, default=u'离线')
	led_enabled = models.BooleanField(default=False)
	led_width = models.IntegerField(default=80)
	led_height = models.IntegerField(default=16)
	action_type = models.SmallIntegerField(default=0)
	action_speed = models.SmallIntegerField(default=0)
	action_border = models.SmallIntegerField(default=False)
	action_blink = models.SmallIntegerField(default=0)
	action_embedded = models.SmallIntegerField(default=0)
	content_text = models.CharField(max_length=4096, default='')
	content_matrix = models.TextField(default='')
	content_status = models.IntegerField(default=255)
	server_feature = models.CharField(max_length=64, null=True, blank=True)
	wechat_enabled = models.BooleanField(default=False)
	alipay_enabled = models.BooleanField(default=False)
	longitude = models.CharField(max_length=16, default='')
	latitude = models.CharField(max_length=16, default='')
	ad_images = models.CharField(max_length=2048, default='')
	ad_links = models.CharField(max_length=4096, default='')
	app_enabled = models.SmallIntegerField(default=0)
	replenishment = models.TextField(blank=True, null=True)
	keyt = models.CharField(max_length=32, blank=True, null=True)
	timeout = models.IntegerField(default=60000)
	page_style = models.CharField(max_length=255, blank=True, null=True)
	title = models.CharField(max_length=255, blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)

	def json(self):
		json_data = {}
		json_data['device'] = self.device
		json_data['status'] = self.status
		if self.team is not None:
			json_data['team'] = self.team.name
			json_data['team_id'] = self.team.team
		else:
			json_data['team_id'] = ''
			json_data['team'] = ''
		json_data['led_enabled'] = (self.led_enabled)[0]
		json_data['led_width'] = self.led_width
		json_data['led_height'] = self.led_height
		json_data['action_type'] = self.action_type
		json_data['action_speed'] = self.action_speed
		json_data['action_border'] = self.action_border
		json_data['action_blink'] = self.action_blink
		json_data['action_embedded'] = self.action_embedded
		json_data['content_text'] = self.content_text
		json_data['content_status'] = self.content_status
		json_data['wechat_enabled'] = (self.wechat_enabled)[0]
		json_data['alipay_enabled'] = (self.alipay_enabled)[0]
		json_data['title'] = self.title
		return json_data

	class Meta:
         db_table='devices'

class authorize_device(models.Model):
	idea = models.AutoField(primary_key=True)
	level = models.IntegerField(default=0)
	device = models.IntegerField(max_length=20)
	user = models.IntegerField(max_length=20)
	org = models.CharField(max_length=20)
	geass_acc = models.BooleanField(default=True)
	geass_state = models.BooleanField(default=True)
	geass_auth = models.BooleanField(default=True)
	geass_sup = models.BooleanField(default=True)
	geass_supm = models.BooleanField(default=True)
	geass_devm = models.BooleanField(default=True)
	geass_devd = models.BooleanField(default=True)

	def json(self):
		json_data = {}
		json_data['org'] = self.org
		json_data['user'] = users.objects.get(user_id=self.user).username
		json_data['geass_acc'] = (self.geass_acc)[0]
		json_data['geass_state'] = (self.geass_state)[0]
		json_data['geass_auth'] = (self.geass_auth)[0]
		json_data['geass_sup'] = (self.geass_sup)[0]
		json_data['geass_supm'] = (self.geass_supm)[0]
		json_data['geass_devm'] = (self.geass_devm)[0]
		json_data['geass_devd'] = (self.geass_devd)[0]
		return json_data

	class Meta:
         db_table='authorize_device'

def get_photo_path(instance, filename):
    userName = instance.user.username
    productionName = userName + datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' +filename.split('.')[1]
    
    return '%s' % (productionName)

class goodsclass(models.Model):
	classify = models.AutoField(primary_key=True)
	user = models.ForeignKey(users, blank=True, null=True, on_delete=models.SET_NULL,db_column='user')
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=256, null=True, blank=True)
	created_at = models.DateTimeField(default=datetime.now)
	class Meta:
         db_table='goodsclass'
         
class goods(models.Model):
	good = models.AutoField(primary_key=True)
	user = models.ForeignKey(users, blank=True, null=True, on_delete=models.SET_NULL, db_column='user')
	name = models.CharField(max_length=256, default='')
	image1 = models.ImageField(upload_to=get_photo_path,max_length=256, blank=True, null=True)
	image2 = models.ImageField(upload_to=get_photo_path,max_length=256, blank=True, null=True)
	image3 = models.ImageField(upload_to=get_photo_path,max_length=256, blank=True, null=True)
	description = models.CharField(max_length=128, default='')
	expire_at = models.DateTimeField(null=True, blank=True)
	purchase_price = models.IntegerField(null=True, blank=True)
	retail_price = models.IntegerField(null=True, blank=True)
	currency = models.CharField(max_length=30, default='CNY')
	created_at = models.DateTimeField(default=datetime.now)
	deleted = models.BooleanField(default=False)
	classify = models.ForeignKey(goodsclass, blank=True, null=True, on_delete=models.SET_NULL,db_column='classify')

	def json(self):
		json_data = {}
		json_data['name'] = self.name
		json_data['image1'] = self.image1.name
		json_data['image2'] = self.image2.name
		json_data['image3'] = self.image3.name
		json_data['description'] = self.description
		json_data['purchase_price'] = (self.purchase_price)/100
		json_data['retail_price'] = (self.retail_price)/100
		json_data['currency'] = self.currency
		if self.expire_at == None:
			json_data['expire_at'] = ''
		else:
			json_data['expire_at'] = self.expire_at.strftime('%Y-%m-%d')
		json_data['goods_id'] = self.good
		json_data['created_at'] = self.created_at.strftime('%Y-%m-%d')
		if self.classify == None:
			json_data['classify'] = ''
		else:
			json_data['classify'] = self.classify.classify
		return json_data

	def idcard(self):
		return self.good

	class Meta:
         db_table='goods'

class cabinets(models.Model):
	cabinet = models.AutoField(primary_key=True)
	sequence = models.IntegerField(null=True, blank=True)
	device = models.ForeignKey(devices, blank=True, null=True, on_delete=models.SET_NULL,db_column='device')
	lockers_count = models.SmallIntegerField(null=True, blank=True)
	description = models.CharField(max_length=256, default='')
	title = models.CharField(max_length=255, blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)

	def json(self):
		json_data = {}
		json_data['device'] = self.device.device
		json_data['sequence'] = self.sequence
		json_data['lockers_count'] = self.lockers_count
		json_data['description'] = self.description
		json_data['headmsg'] = self.title
		json_data['bodymsg'] = self.name
		return json_data

	class Meta:
         db_table='cabinets'

class lockers(models.Model):
	locker = models.AutoField(primary_key=True)
	sequence = models.SmallIntegerField(null=True, blank=True)
	cabinet = models.ForeignKey(cabinets, blank=True, null=True, on_delete=models.SET_NULL,db_column='cabinet')
	good = models.ForeignKey(goods, blank=True, null=True, on_delete=models.SET_NULL,db_column="good")
	failure = models.BooleanField(default=False)
	opening = models.BooleanField(default=False)
	latest_sell = models.DateTimeField(null=True,blank=True)
	latest_restocking = models.DateTimeField(null=True,blank=True)
	expire_at = models.DateTimeField(null=True, blank=True)
	retail_price = models.IntegerField(null=True, blank=True)
	currency = models.CharField(max_length=30, default='CNY')
	draw_rate = models.SmallIntegerField(default=0)
	
	class Meta:
         db_table='lockers'

class orders(models.Model):
	trade_no = models.CharField(max_length=32, default='')
	platform_trade_no = models.CharField(max_length=64, default='')
	refund_trade_no = models.CharField(max_length=32, null=True, blank=True)
	refund_platform_trade_no = models.CharField(max_length=64, null=True, blank=True)
	merchant_no = models.CharField(max_length=32, default='')
	created_at = models.DateTimeField(default=datetime.now)
	payed_at = models.DateTimeField(null=True, blank=True)
	refunded_at = models.DateTimeField(null=True, blank=True)
	payed = models.BooleanField(default=False)
	communication_succeeded = models.BooleanField(default=False)
	refunded = models.BooleanField(default=False)
	draw = models.BooleanField(default=False)
	customer1 = models.CharField(max_length=32, default='')
	customer2 = models.CharField(max_length=256, default='')
	device = models.ForeignKey(devices, blank=True, null=True, on_delete=models.SET_NULL,db_column='device')
	user = models.ForeignKey(users, blank=True, null=True, on_delete=models.SET_NULL,db_column='user')
	payment_channel = models.CharField(max_length=32, default='')
	initial_amount = models.IntegerField(null=True, blank=True)
	rate = models.IntegerField(default=100)
	discounted_amount = models.IntegerField(null=True, blank=True)
	currency = models.CharField(max_length=30, default='CNY')
	description = models.CharField(max_length=256, default='')
	remark = models.CharField(max_length=256, null=True,blank=True)

	class Meta:
         db_table='orders'

class operation_logs(models.Model):
	# locker = models.ForeignKey(lockers, blank=True, null=True, on_delete=models.SET_NULL,db_column='locker') #maybe manytomany
	cabinet = models.SmallIntegerField(null=True, blank=True)
	locker = models.SmallIntegerField(null=True, blank=True)
	device = models.ForeignKey(devices, blank=True, null=True, on_delete=models.SET_NULL,db_column='device')
	order = models.ForeignKey(orders, blank=True, null=True, on_delete=models.SET_NULL,db_column='order')
	timestamp = models.DateTimeField(blank=True, null=True)
	good = models.ForeignKey(goods,blank=True, null=True, on_delete=models.SET_NULL,db_column='good')
	amount = models.IntegerField(default=0)
	currency = models.CharField(max_length=30, default='CNY')
	description = models.CharField(max_length=128, default='')

	class Meta:
         db_table='operation_logs'

class withdrawals(models.Model):
	trade_no = models.CharField(max_length=32,unique=True)
	user = models.ForeignKey(users, blank=True, null=True, on_delete=models.SET_NULL,db_column='user')
	payment_channel = models.CharField(max_length=32,null=True,blank=True)
	amount = models.IntegerField(default=0)
	auxiliary = models.IntegerField(default=0)
	account = models.CharField(max_length=256,null=True,blank=True)
	account_name = models.CharField(max_length=256,null=True,blank=True)
	period_from = models.DateTimeField(blank=True, null=True)
	period_to = models.DateTimeField(blank=True, null=True)
	succeeded = models.BooleanField(default=False)
	description = models.CharField(max_length=256,null=True,blank=True)

	class Meta:
         db_table='withdrawals'