<template>
  <el-aside style="background-color: rgba(238, 238, 238, 0.98); width: 200px;">
  	<el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @select="addNewTab"
      background-color="rgba(238, 238, 238, 0.98)"
      active-text-color="#409EFF">
      <el-submenu index="1" v-if="leftItem.one.show">
        <template slot="title">
          <i class="el-icon-setting"></i>
          <span>管理员设置</span>
        </template>
      <el-menu-item index="group" v-if="leftItem.one.instIndex">机构管理</el-menu-item>
      <el-menu-item index="users" v-if="leftItem.one.userIndex">用户管理</el-menu-item>
      <el-menu-item index="status" v-if="leftItem.one.statusIndex">角色管理</el-menu-item>
      </el-submenu>
      <el-submenu index="2" v-if="leftItem.two.show">
        <template slot="title">
          <i class="el-icon-goods"></i>
          <span>产品管理</span>
        </template>
      <el-menu-item index="device" v-if="leftItem.two.deviceIndex">设备管理</el-menu-item>
      <el-menu-item index="goods" v-if="leftItem.two.goodsIndex">商品管理</el-menu-item>
      <el-menu-item index="goods_pipe" v-if="leftItem.two.goods_pipeIndex">货道管理</el-menu-item>
      </el-submenu>
      <el-submenu index="3" v-if="leftItem.three.show">
        <template slot="title">
          <i class="el-icon-date"></i>
          <span>数据分析</span>
        </template>
      <el-menu-item index="order" v-if="leftItem.three.orderIndex">订单记录</el-menu-item>
      <el-menu-item index="customer" v-if="leftItem.three.customerIndex">客流统计</el-menu-item>
      <el-menu-item index="achieve" v-if="leftItem.three.achieveIndex">财务报表</el-menu-item>
      </el-submenu>
    </el-menu>
  </el-aside>
</template>
<script>
  import {mapState, mapMutations} from 'vuex'
  import {translate} from 'common/js/config'

	export default {
    props: {
      leftItem: {
        default: {
          one: {
            show: false,
            instIndex: false,
            userIndex: false,
            statusIndex: false
          },
          two: {
            show: false,
            deviceIndex: false,
            goodsIndex: false,
            goods_pipeIndex: false
          },
          three: {
            show: false,
            orderIndex: false,
            customerIndex: false,
            achieveIndex: false
          }
        }
      }
    },
		computed: {
      ...mapState([
        'tabList',
        'activate'
      ])
    },
    methods: {
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

