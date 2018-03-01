<template>
	<transition name="page">
		<section id="banner">
			<div class="bannerTop">
				<div class="device">
					<div class="deviceLeft">
						<div class="owl"></div>
					</div>
					<div class="deviceRight">
						<div class="deviceInfo"><span class="deviceName">共享充电系统</span> <span class="deviceNum">{{ device }}</span></div>
						<div class="deviceRemark">访问访问</div>
					</div>
				</div>
				<div class="btnGroup">
					<div class="divBtn" v-for="item in msg" :class="{'active':radiohead === item.sequence}" @click="changeRadio(item.sequence)" :label="item.sequence"><span class="remark">{{ item.remark }}</span><span class="price">￥ {{ item.retail_price }}</span></div>
				</div>
				<div class="rate"><span class="rateL">会员折扣</span><span class="rateR">暂无可用折扣</span></div>
			</div>
			<div class="bannerMid">
				<div class="payImg"></div><div class="payRadio"><el-radio v-model="radioNeck" label=""></el-radio></div>
				<!-- <el-radio-button v-model="" :label="">微信支付</span></el-radio-button> -->
			</div>
			<div class="bannerbottom">
				<el-button type="primary" round>立即充电</el-button>
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
	  		radioNeck: '',
	  		msg: [{'remark': '充电一小时', 'sequence': 1, 'retail_price': 1.0}],
	  		isChange: false
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
	  	changeRadio (val) {
	  		this.radiohead = val
	  		console.log(this.radiohead)
	  	},
	  	refreshWeb () {
	  		window.location.href = '/pay/re_paying/?device=' + this.device
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
	  			let that = this
		  		WeixinJSBridge.invoke('getBrandWCPayRequest', {
			      'appId': jsonobj.appId, // 公众号名称，由商户传入
			      'timeStamp': jsonobj.timeStamp, // 时间戳
			      'nonceStr': jsonobj.nonceStr, // 随机串
			      'package': jsonobj.package, // 扩展包
			      'signType': jsonobj.signType, // 微信签名方式:1.sha1
			      'paySign': jsonobj.paySign// 微信签名
			    }, function (res) {
			      if (res.err_msg === 'get_brand_wcpay_request:ok') {
						  sendData({'device': that.device, 'sequence': that.radiohead}, '/sendMQ').then((res) => {
						  	if (res.data.device === that.device && res.data.sequence === that.radiohead) {
							  	that.$message({
										message: '支付成功',
										type: 'success',
								    showClose: true
								  })
								  alert(res.data.sequence)
						  	}
						  })
						  
			      } else {
			      	that.$message({
								message: '错误：' + '支付失败',
								type: 'error',
						    showClose: true
						  })
						  setTimeout(() => {
						  	that.refreshWeb()
						  }, 1000)
			      }
			    })
		  	})
	  	},
	  	payBtn () {
	  		this.payLoad = true
	  		this.isChange = true
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
		background: rgb(240, 240, 240)
		.bannerTop
			padding: 1em
			background: white
			.device
				background: white
				display: flex
				margin-bottom: 0.5em
				.deviceLeft
					flex:0 0 100px
					height: 100px
					box-sizing: border-box
					text-align: center
					.owl
						width: 80px
						height: 80px
						margin: 10px 0 0 10px
						border-radius: 50%
						background: url('~common/img/owl.jpg') no-repeat center center
						background-size: 100% 100%
				.deviceRight
					flex:1
					.deviceInfo
						height: 60px
						line-height: 80px
						.deviceName
							font-weight: 600
						.deviceNum
							float:right
							color: rgb(144,144,144)
					.deviceRemark
						height: 40px
						color: rgb(144,144,144)
						font-size: 14px
			.btnGroup
				.divBtn
					width: 100%
					height: 80px
					line-height: 80px
					margin: 0 0 0.5em 0
					border-radius: 4px
					box-sizing: border-box
					background: -webkit-linear-gradient(left, #A2B5CD , 	#B8B8B8); /* Safari 5.1 - 6.0 */
					background: -o-linear-gradient(right, #A2B5CD, 	#B8B8B8); /* Opera 11.1 - 12.0 */
					background: -moz-linear-gradient(right, #A2B5CD, 	#B8B8B8); /* Firefox 3.6 - 15 */
					background: linear-gradient(to right, #A2B5CD , 	#B8B8B8); /* 标准的语法（必须放在最后） */
					color: rgb(244,244,244)
					&.active
						background: -webkit-linear-gradient(left, #409EFF , #4169E1); /* Safari 5.1 - 6.0 */
						background: -o-linear-gradient(right, #409EFF, #4169E1); /* Opera 11.1 - 12.0 */
						background: -moz-linear-gradient(right, #409EFF, #4169E1); /* Firefox 3.6 - 15 */
						background: linear-gradient(to right, #409EFF , #4169E1); /* 标准的语法（必须放在最后） */
						color: #fff
					.remark, .price
						height: 20px
						line-height: 20px
						display: inline-block
						box-sizing: border-box
					.remark
						width: 80%
						padding-left: 30px
					.price
						width: 20%
						text-align: right
						padding-right: 30px
			.rate
				font-size: 14px
				margin-top: 3em
				.rateL, .rateR
					display: inline-block
					width: 50%
				.rateR
					text-align: right
					color: rgb(133,133,133)
		.bannerMid
			margin-top: 1em
			height: 80px
			background: white
			.payImg
				height: 40px
				width: 70%
				display: inline-block
				background: url('~common/img/wechat.png') no-repeat left center
				background-size: 148px 40px
				margin: 20px 0 0 20px
			.payRadio
				margin: 20px 20px 0 0
				height: 40px
				line-height: 40px
				float: right
				display: inline-block
				.el-radio
					>>> .el-radio__input
						.el-radio__inner
							height: 25px
							width: 25px
		.bannerbottom
			padding: 1em
			.el-button
				width: 100%
				height: 50px
				font-size: 1em
				letter-spacing: 0.1em
	.page-enter-active
		transition: all 0.2s ease
	.page-enter
		opacity: 0
</style>