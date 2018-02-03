<template>
	<div>
		<el-button type="success" @click="pay">点击支付 {{ this.$route.params.num }}</el-button>
	</div>
</template>
<script>
	import {sendData} from 'api/data'

	export default {
	  name: 'home',
	  data () {
	  	return {
	  	}
	  },
	  method: {
	  	onBridgeReady () {
	  		let url = '/paydetail'
	  		let data = {'device': this.$route.params.num}

	  		sendData(data, url).then((res) => {
	  			console.log(res)
	  			let jsonobj = res
		  		WeixinJSBridge.invoke('getBrandWCPayRequest', {
			      'appId': jsonobj.appId, // 公众号名称，由商户传入
			      'timeStamp': jsonobj.timestamp, // 时间戳
			      'nonceStr': jsonobj.nonceStr, // 随机串
			      'package': jsonobj.package, // 扩展包
			      'signType': 'MD5', // 微信签名方式:1.sha1
			      'paySign': jsonobj.paySign// 微信签名
			    }, function (res) {
			      if (res.err_msg === 'get_brand_wcpay_request:ok') {
			        this.$message({
								message: '支付成功',
								type: 'success',
						    showClose: true
						  })
			      } else {
			      	this.$message({
								message: '错误：' + res.err_msg,
								type: 'error',
						    showClose: true
						  })
			      }
			    })
		  	})
	  	},
	  	pay () {
	  		if (typeof WeixinJSBridge === 'undefined') {
				  if (document.addEventListener) {
				    document.addEventListener('WeixinJSBridgeReady', this.onBridgeReady(), false)
				  } else if (document.attachEvent) {
				    document.attachEvent('WeixinJSBridgeReady', this.onBridgeReady())
				    document.attachEvent('onWeixinJSBridgeReady', this.onBridgeReady())
				  }
				} else {
				  this.onBridgeReady()
				}
	  	}
	  },
	  components: {
	  }
	}
</script>
