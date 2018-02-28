<template>
	<transition name="page">
		<section id="banner">
			<div class="inner">
				<h2>Powerbank</h2>
				<p>点击按钮支付成功后获取密码！<br />
				设备编号: {{ device }}<br />
				</p>
				<div style="margin-bottom: 30px">
					<el-radio v-for="item in msg"
					style="margin: 0 0 10px 0; display: block; text-align: left; background:white"
					v-model="radiohead"
					:label="item.sequence"
					border
					>{{ item.name }}  {{ item.goods_name }} 售价: {{ item.retail_price }} 元 {{ item.remark }}</el-radio>
				</div>
				<ul>
					<el-button class="actions" type="danger" :loading="payLoad" :disabled="paySub" @click="payBtn">激  活</el-button>
				</ul>
			</div>
		</section>
	</transition>
</template>
<script>
	import {sendData} from 'api/data'

	export default {
	  name: 'pay',
	  data () {
	  	return {
	  		device: this.$route.query.device,
	  		code: this.$route.query.code,
	  		payLoad: false,
	  		paySub: true,
	  		radiohead: 1,
	  		msg: []
	  	}
	  },
	  created () {
	  	this._getPayinfo()
	  },
	  methods: {
	  	_getPayinfo () {
	  		let device = this.device
	  		let url = '/payinfo'
	  		sendData({'device': device}, url).then((res) => {
	  			if (res.err_msg === 'ok') {
	  				this.msg = res.msg
	  				this.paySub = false
	  			}
	  		})
	  	},
	  	onBridgeReady () {
	  		let url = '/paydetail'
	  		let data = {
	  			'device': this.device,
	  			'sequence': this.radiohead,
	  			'code': this.code
	  		}
	  		sendData(data, url).then((res) => {
	  			let jsonobj = res
		  		WeixinJSBridge.invoke('getBrandWCPayRequest', {
			      'appId': jsonobj.appId, // 公众号名称，由商户传入
			      'timeStamp': jsonobj.timeStamp, // 时间戳
			      'nonceStr': jsonobj.nonceStr, // 随机串
			      'package': jsonobj.package, // 扩展包
			      'signType': jsonobj.signType, // 微信签名方式:1.sha1
			      'paySign': jsonobj.paySign// 微信签名
			    }, function (res) {
			      if (res.err_msg === 'get_brand_wcpay_request:ok') {
			        this.$message({
								message: '支付成功',
								type: 'success',
						    showClose: true
						  })
						  sendData({'device': this.device, 'sequence': this.radiohead}, '/sendMQ').then((res) => {

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
	  	payBtn () {
	  		this.payLoad = true
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
<style scoped lang="stylus" rel="stylesheet/stylus">
	#banner
		top: 0
		left: 0
		right: 0
		bottom: 0
		position: fixed
		background-image: -webkit-linear-gradient(top, rgba(0,0,0,0.5), rgba(0,0,0,0.5)),url("./banner.jpg")
		background-position: center center
		background-repeat: no-repeat
		background-size: cover
		padding: 7em 3em 5em 3em
		.inner
			text-align: center
			color: white
			p
				margin: 0 0 2em
				line-height: 1.65em
				font-weight: 400
			h2
				font-weight: 800
				letter-spacing: 0.225em
				margin: 0 0 1em 0
				text-transform: uppercase
				font-size: 1.25em
				padding: 0.35em 1em
				line-height: 1.65em
				position: relative
				display: inline-block
				&:before, &:after
					// -moz-transition: width 0.85s ease;
					// -webkit-transition: width 0.85s ease;
					// -ms-transition: width 0.85s ease;
					// transition: width 0.85s ease;
					// -moz-transition-delay: 0.25s;
					// -webkit-transition-delay: 0.25s;
					// -ms-transition-delay: 0.25s;
					// transition-delay: 0.25s;
					background: #fff
					content: ''
					display: block
					height: 2px
					position: absolute
					width: 100%
				&:before
					top: 0
					left: 0
				&:after
					bottom: 0
					right: 0
			ul
				font-weight: 500
				.actions
					width: 100%
	.page-enter-active
		transition: all 0.2s ease
	.page-enter
		opacity: 0
</style>