<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'app'
  }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" rel="stylesheet/stylus">
	.el-table
		width: 100%
		min-height: 540px
	.block .el-pagination
		text-align: center
		padding: 10px 0
		
	.toolbar 
		background: #f2f2f2
		padding: 10px
		//border:1px solid #dfe6ec;
		margin: 10px 0px
		.el-form-item 
			margin-bottom: 10px
</style>