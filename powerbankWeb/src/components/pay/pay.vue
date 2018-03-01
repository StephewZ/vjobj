<template>
	<div>
		<paypb v-if="webtype === 2"></paypb>
		<paydrink v-if="webtype === 1"></paydrink>
		<!-- <router-view></router-view> -->
	</div>
</template>
<script>
	import {sendData} from 'api/data'
	import Paypb from 'components/paypb/paypb'
	import Paydrink from 'components/paydrink/paydrink'

	export default {
	  name: 'pay',
	  data () {
	  	return {
	  		webtype: +this.$route.query.webtype
	  	}
	  },
	  created () {
	  	this.test()
	  },
	  methods: {
	  	test() {
	  		console.log(this.$route.query.webtype)
	  		console.log(this.$route.query.webtype === '1')
	  	}
	  },
	  components: {
	  	Paypb,
	  	Paydrink
	  }
	}
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">

</style>