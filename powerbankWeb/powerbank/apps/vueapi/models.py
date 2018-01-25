#-*-encoding:utf-8 -*-
from django.db import models
from datetime import datetime

# Create your models here.


class device_inst(models.Model):
	device_id = models.IntegerField(null=True, blank=True)
	inst_id = models.IntegerField(null=True, blank=True)
	auth_type = models.IntegerField(default=1)
	remark = models.CharField(max_length=255, default='') #备注

	class Meta:
		db_table='device_inst'