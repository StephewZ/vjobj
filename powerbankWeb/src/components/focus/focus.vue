<template>
	<el-container id="container">
    <el-header class="title">
      <span>后台管理平台</span>
      <el-dropdown trigger="click">
          <span class="el-dropdown-link userinfo-inner">{{ nickname }}</span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>我的消息</el-dropdown-item>
            <el-dropdown-item>设置</el-dropdown-item>
            <el-dropdown-item divided @click.native="_logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
    </el-header>
      <el-container>
        <navs></navs>
        <tab></tab>
      </el-container> 
  </el-container>
</template>

<script>
  import Tab from 'components/tab/tab'
  import Navs from 'components/navs/navs'
  import {getData} from 'api/data'
  import {logout} from 'api/userEvent'
  import {ERR_OK, urls} from 'api/config'

  export default {
    data () {
      return {
        nickname: ''
      }
    },
    created () {
      this._getUserinfo(urls.userinfo.tips, urls.userinfo.url)
    },
    methods: {
      _getUserinfo (tip, url) {
        getData(tip, url).then((res) => {
          if (res.code === ERR_OK) {
            this.nickname = res.data.nickname
          }
        })
      },
      _logout () {
        logout(urls.logout.url).then((res) => {
          if (res.code === ERR_OK) {
            window.location.reload()
          }
        })
      }
    },
    components: {
      Navs,
      Tab
    }
  }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="stylus" rel="stylesheet/stylus">
  #container
    position: absolute
    top: 0
    bottom: 0
    width: 100%
    .title
      height: 50px !important
      line-height: 50px
      background-color: rgb(2, 2, 2)
      color: rgb(244,244,244)
      .el-dropdown
        float: right
        .userinfo-inner
          cursor: pointer
          color: #fff
</style>