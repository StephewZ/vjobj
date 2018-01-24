<template>
  <el-aside style="background-color: rgba(238, 238, 238, 0.98); width: 200px;">
  	<el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      @select="addNewTab"
      background-color="rgba(238, 238, 238, 0.98)"
      active-text-color="#409EFF">
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-setting"></i>
          <span>管理员设置</span>
        </template>
      <el-menu-item index="group">机构管理</el-menu-item>
      <el-menu-item index="users">用户管理</el-menu-item>
      <el-menu-item index="status">角色管理</el-menu-item>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-goods"></i>
          <span>产品管理</span>
        </template>
      <el-menu-item index="device">设备管理</el-menu-item>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">
          <i class="el-icon-date"></i>
          <span>数据分析</span>
        </template>
      <el-menu-item index="order">订单记录</el-menu-item>
      <el-menu-item index="3-2">2</el-menu-item>
      <el-menu-item index="3-3">3</el-menu-item>
      </el-submenu>
    </el-menu>
  </el-aside>
</template>
<script>
  import {mapState, mapMutations} from 'vuex'
  import {translate} from 'common/js/config'

	export default {
		computed: {
      ...mapState([
        'tabList',
        'activate'
      ])
    },
    methods: {
    	handleOpen (key, keyPath) {
        console.log(key, keyPath)
      },
      handleClose (key, keyPath) {
        console.log(key, keyPath)
      },
      addNewTab (targetName, index) {
      	index = index[1]
      	if (this.tabList.filter(f => f.name === index).length === 0) {
      		let component = resolve => require([`components/${index}/${index}`], resolve)
      		let newtabList = this.tabList.slice()
      		newtabList.push({
            label: translate[index],
            name: index,
            closable: true,
            component: component
	        })
	        this.addTab(newtabList)
	        this.turnTo(index)
      	} else if (this.activate !== index) {
      		this.turnTo(index)
      	}
      },
	    ...mapMutations({
	      'addTab': 'ADD_TAB',
	      'turnTo': 'TURN_TO'
	    })
    }
	}
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
  .el-main
    padding: 0
  .el-menu
    >>> .el-submenu__title
      height: 40px
      line-height: 40px
      color: #333
      border-bottom: 1px solid #e5e5e5
    >>> .el-menu-item
      height: 30px
      line-height: 30px
      color: #666
      padding-left: 60px !important 
</style>

