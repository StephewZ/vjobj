<template>
	<div class="setting">
		<crumb :crumbMsg="crumbMsg"></crumb>
		<div class="parentDiv">
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
	      <el-form-item>
	      	<el-button type="primary" @click="setSubmit('setForm')" :loading="setLoading" size="small">提交</el-button>
	      </el-form-item>
	    </el-form>
    </div>
  </div>
</template>
<script>
	import Crumb from 'components/crumb/crumb'
	import {sendData} from 'api/data'
	import {urls, ERR_OK} from 'api/config'
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
		  	crumbMsg: ['设置'],
		  	setForm: {
          pass: '',
          newPass: '',
          checkPass: ''
        },
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
		methods: {
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
	  	Crumb
	  }
	}
</script>
<style coped lang="stylus" rel="stylesheet/stylus">
	.parentDiv
		padding: 10px
</style>