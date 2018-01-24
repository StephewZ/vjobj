<template>
	<div class='crumb'>
		<el-breadcrumb separator=">">
		  <el-breadcrumb-item>主页</el-breadcrumb-item>
		  <el-breadcrumb-item v-for="msg in crumbMsg" :key="msg">{{ msg }}</el-breadcrumb-item>
		</el-breadcrumb>
	</div>
</template>
<script>
	export default {
	  name: 'device',
	  props: ['crumbMsg']
	}
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
	.crumb
		background: #f5f5f5
		padding: 10px
</style>