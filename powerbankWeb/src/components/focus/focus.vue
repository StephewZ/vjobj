<template>
	<el-container id="container">
    <el-header class="title">
      <span>后台管理平台</span>
      <el-dropdown trigger="click">
        <span class="el-dropdown-link userinfo-inner">{{ nickname }}</span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>我的消息</el-dropdown-item>
          <el-dropdown-item @click="handleSet">设置</el-dropdown-item>
          <el-dropdown-item divided @click.native="_logout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-header>
    <el-container>
      <navs :leftItem="leftItem"></navs>
      <tab></tab>
    </el-container>
    <el-dialog title="设置" :visible.sync="setFormVisible" :close-on-click-modal="true">
      <el-form :model="setForm" label-width="80px" :rules="FormRules" ref="setForm">
        <el-form-item label="旧的密码" prop="pass">
          <el-input type="password" maxlength="15" v-model="setForm.pass" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="新的密码" prop="newPass">
          <el-input type="password" maxlength="15" v-model="setForm.newPass" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" maxlength="15" v-model="setForm.checkPass" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="setFormVisible = false" size="small">取消</el-button>
        <el-button type="primary" @click="setSubmit('setForm')" :loading="setLoading" size="small">提交</el-button>
      </div>
    </el-dialog>
  </el-container>
</template>

<script>
  import Tab from 'components/tab/tab'
  import Navs from 'components/navs/navs'
  import {getData, sendData} from 'api/data'
  import {logout} from 'api/userEvent'
  import {ERR_OK, urls} from 'api/config'
  import {msgNotice} from 'common/js/dom'

  export default {
    data () {
      let validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入旧的密码'))
        } else if (value.length < 6) {
          callback(new Error('密码长度至少为6位'))
        } else {
          if (this.setForm.checkPass !== '') {
            this.$refs.setForm.validateField('checkPass')
          }
          callback()
        }
      }
      let validatenewPass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入新的密码'))
        } else if (value.length < 6) {
          callback(new Error('密码长度至少为6位'))
        } else {
          if (this.setForm.checkPass !== '') {
            this.$refs.setForm.validateField('checkPass')
          }
          callback()
        }
      }
      let validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'))
        } else if (value !== this.setForm.newPass) {
          callback(new Error('两次输入密码不一致!'))
        } else {
          callback()
        }
      }
      return {
        nickname: '',
        setForm: {
          pass: '',
          newPass: '',
          checkPass: ''
        },
        setFormVisible: false,
        setLoading: false,
        FormRules: {
          pass: [
            { required: true, validator: validatePass, trigger: 'blur' }
          ],
          newPass: [
            { required: true, validator: validatenewPass, trigger: 'blur' }
          ],
          checkPass: [
            { required: true, validator: validatePass2, trigger: 'blur' }
          ]
        }
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
            this.leftItem = res.data.leftItem
          }
        })
      },
      _logout () {
        logout(urls.logout.url).then((res) => {
          if (res.code === ERR_OK) {
            window.location.reload()
          }
        })
      },
      handleSet () {
        console.log(this.setFormVisible)
        this.setFormVisible = true
      },
      setSubmit (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let tip = urls.userNavs.tips
            let url = urls.userNavs.url
            const data = Object.assign({}, tip, this.setForm)
            sendData(data, url).then((res) => {
              if (res.code === ERR_OK) {
                msgNotice(res.data.err, 'success', false, false, this)
              } else {
                msgNotice(res.data.err, 'error', false, false, this)
              }
            })
          } else {
            msgNotice('发生错误，请刷新页面重试！', 'error', false, false, this)
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