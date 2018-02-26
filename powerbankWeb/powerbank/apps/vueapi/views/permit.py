from users.models import users, institutions, status_user, status_module, status, funcmodule

authList = {
	'admin': '0',
	'instIndex': '0.001.001.004',
	'instAdd': '0.001.001.001',
	'instDel': '0.001.001.002',
	'instEdit': '0.001.001.003',
	'instList': '0.001.001.004',
	'userIndex': '0.001.002.004',
	'userAdd': '0.001.002.001',
	'userDel': '0.001.002.002',
	'userEdit': '0.001.002.003',
	'userList': '0.001.002.004',
	'statusIndex': '0.001.003.004',
	'statusAdd': '0.001.003.001',
	'statusDel': '0.001.003.002',
	'statusEdit': '0.001.003.003',
	'statusList': '0.001.003.004',
	'deviceIndex': '0.002.001.004',
	'deviceAdd': '0.002.001.001',
	'deviceDel': '0.002.001.002',
	'deviceEdit': '0.002.001.003',
	'deviceList': '0.002.001.004',
	'goodsIndex': '0.002.002.004',
	'goodsAdd': '0.002.002.001',
	'goodsDel': '0.002.002.002',
	'goodsEdit': '0.002.002.003',
	'goodsList': '0.002.002.004',
	'goodsPipeIndex': '0.002.003.004',
	'goodsPipeAdd': '0.002.003.001',
	'goodsPipeDel': '0.002.003.002',
	'goodsPipeEdit': '0.002.003.003',
	'goodsPipeList': '0.002.003.004',
	'orderUpload': '0.003.001.001',
	'orderIndex': '0.003.001.002',
	'customerUpload': '0.003.002.001',
	'customerIndex': '0.003.002.002',
	'achieveUpload': '0.003.003.001',
	'achieveIndex': '0.003.003.002'
}


def Authentication(auth, user):
	pipe_id = authList[auth]
	status_id_list = status_user.objects.filter(user_id = user.id, status_id__in=status.objects.filter(is_enabled=True).values_list('id')).values_list('status_id')
	if status_module.objects.filter(status_id__in = status_id_list, module_id = funcmodule.objects.get(pipe_id=pipe_id,is_enabled=True).id).exists():
		return True
	else:
		return False