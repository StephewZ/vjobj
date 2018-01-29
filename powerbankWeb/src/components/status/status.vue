<template>
  <div>
		<crumb :crumbMsg="crumbMsg"></crumb>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true">
				<el-form-item>
					<el-cascader
				    placeholder="请选择机构"
				    :options="options"
				    v-model="filters.optFilters"
				    filterable
				    change-on-select
				    :disabled="this.loadOn.tableLoading"
				  ></el-cascader>
				</el-form-item>
				<el-form-item>
					<el-input
					  placeholder="请输入查找内容"
					  v-model="filters.mixing"
					  clearable>
					</el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="mini" v-on:click="searchBtn" icon="el-icon-search" :loading="loadOn.searchLoad" :disabled="this.loadOn.tableLoading">查询</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="mini" @click="selectReset" icon="el-icon-refresh" :loading="loadOn.resetLoad" :disabled="this.loadOn.tableLoading">重置</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<el-col type="flex" class="row-bg toolbar" justify="space-between">
			<el-col :span="4">
				<el-button-group>
					<el-button type="danger" size="mini" @click="handleDels" :disabled="this.msgList.length===0 || this.loadOn.tableLoading">批量删除</el-button>
		  		<el-button size="mini" @click="handleAdd" :disabled="this.loadOn.tableLoading">添加</el-button>
	  		</el-button-group>
  		</el-col>
  		<el-col :span="10">
  			<el-button-group>
				  <!-- <el-button type="success" size="mini" icon="el-icon-upload">导入</el-button>
				  <el-button type="" size="mini" style="color:#409EFF">导出<i class="el-icon-download el-icon--right"></i></el-button> -->
				</el-button-group>
			</el-col=>
			<el-col :span="10" style="text-align: right">
				<el-button type="success" round size="mini" @click="refreshPage" :loading="refreshLoad"><i class="el-icon-refresh el-icon--left"></i>刷新</el-button>
			</el-col>
		</el-col>

		<el-table :data="msgList" highlight-current-row v-loading="loadOn.tableLoading" @sort-change="sortChange" @selection-change="selectChange">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column type="index">
			</el-table-column>
			<el-table-column
	      label="信息">
	      <template slot-scope="scope">
	        <el-popover trigger="hover" placement="top">
	          <p>昵称: {{ scope.row.nickname }}</p>
	          <p>电话: {{ scope.row.phone }}</p>
	          <p>地址: {{ scope.row.address }}</p>
	          <p>描述: {{ scope.row.remark }}</p>
	          <div slot="reference" class="name-wrapper">
	            <el-tag size="medium">{{ scope.row.nickname }}</el-tag>
	          </div>
	        </el-popover>
	      </template>
	    </el-table-column>
			<el-table-column prop="username" label="账号">
			</el-table-column>
			<el-table-column prop="inst_name" label="所属机构">
			</el-table-column>
			<el-table-column prop="creator" label="创建用户">
			</el-table-column>
			<el-table-column prop="last_login" label="最近登录" sortable="custom">
			</el-table-column>
			<el-table-column label="操作">
				<template slot-scope="scope">
					<el-button-group>
						<el-button size="small"  @click="handleEdit(scope.row)">编辑</el-button>
						<el-button type="danger" size="small" @click="handleDel(scope.row)">删除</el-button>
					</el-button-group>
				</template>
			</el-table-column>
		</el-table>
		<div class="block">
	    <el-pagination
	      @size-change="handleSizeChange"
	      @current-change="handleCurrentChange"
	      :current-page="filters.currentPage"
	      :page-sizes="[10, 25, 50, 100, total]"
	      :page-size="filters.pageSize"
	      layout="total, sizes, prev, pager, next, jumper"
	      :total="total">
	    </el-pagination>
	  </div>

	  <!--添加界面-->
		<el-dialog title="添加账号" :visible.sync="loadOn.addFormVisible" :close-on-click-modal="true">
			<el-form :model="addForm" label-width="80px" ref="addForm" :rules="FormRules">
				<el-form-item label="昵称" prop="nickname">
					<el-input v-model="addForm.nickname" maxlength="50" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="用户名" prop="username">
					<el-input
					  v-model="addForm.username">
					</el-input>
				</el-form-item>
				<el-form-item label="密码" prop="pass">
			    <el-input type="password" maxlength="15" v-model="addForm.pass" auto-complete="off"></el-input>
			  </el-form-item>
			  <el-form-item label="确认密码" prop="checkPass">
			    <el-input type="password" maxlength="15" v-model="addForm.checkPass" auto-complete="off"></el-input>
			  </el-form-item>
				<el-form-item label="电话" prop="phone">
					<el-input
						placeholder="联系电话"
						maxlength="20"
					  v-model="addForm.phone">
					</el-input>
				</el-form-item>
				<el-form-item label="联系地址" prop="address">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="addForm.address"
					  placeholder="联系地址">
					</el-input>
				</el-form-item>
				<el-form-item label="所属机构" prop="pipe">
					<el-cascader
				    placeholder="请选择机构"
				    :options="options"
				    filterable
				    v-model="addForm.pipe"
				    change-on-select
				  ></el-cascader>
				</el-form-item>
				<el-form-item label="描述" prop="remark">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="addForm.remark"
					  placeholder="机构描述">
					</el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="loadOn.addFormVisible = false" size="small">取消</el-button>
				<el-button type="primary" @click="addSubmit('addForm')" :loading="loadOn.addLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

	  <!--编辑界面-->
		<el-dialog title="账号设置" :visible.sync="loadOn.editFormVisible" :close-on-click-modal="true">
			<el-form :model="editForm" label-width="80px" :rules="FormRules" ref="editForm">
				<el-form-item label="昵称" prop="nickname">
					<el-input v-model="editForm.nickname" maxlength="50" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="用户名" prop="username">
					<el-input
					  v-model="editForm.username"
					  :disabled="true">
					</el-input>
				</el-form-item>
				<el-form-item label="电话" prop="phone">
					<el-input
						placeholder="联系电话"
						maxlength="20"
					  v-model="editForm.phone">
					</el-input>
				</el-form-item>
				<el-form-item label="联系地址" prop="address">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="editForm.address"
					  placeholder="联系地址">
					</el-input>
				</el-form-item>
				<el-form-item label="所属机构" prop="pipe">
					<el-cascader
				    placeholder="请选择机构"
				    :options="options"
				    filterable
				    v-model="editForm.pipe"
				    change-on-select
				  ></el-cascader>
				</el-form-item>
				<el-form-item label="描述" prop="remark">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="editForm.remark"
					  placeholder="描述">
					</el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="loadOn.editFormVisible = false" size="small">取消</el-button>
				<el-button type="primary" @click="editSubmit" :loading="loadOn.editLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

  </div>
</template>
<script>
	import Crumb from 'components/crumb/crumb'
	import {getData, sendData} from 'api/data'
	import {urls, ERR_OK} from 'api/config'
	import {formatList, comparePipe, msgNotice} from 'common/js/dom'

	export default {
	  name: 'group',
	  data () {
	  	return {
	  		crumbMsg: ['管理员管理', '角色管理'],
	  		filters: {
	  			'optFilters': [],
	  			'mixing': '',
	  			'pageSize': 10,
	  			'currentPage': 1,
	  			'sortName': '',
	  			'orderType': ''
	  		},
	  		loadOn: {
	  			'tableLoading': true,
	  			'addFormVisible': false,
        	'editFormVisible': false,
        	'editLoading': false,
        	'addLoading': false,
        	'searchLoad': false,
        	'resetLoad': false,
        	'refreshLoad': false
	  		},
	  		total: 0,
	  		msgList: [],
	  		delList: [],
	  		options: [],
        FormRules: {
					nickname: [
						{ required: true, message: '请输入用户昵称', trigger: 'blur' },
						{ min: 2, max: 25, message: '长度在 2 到 25 个字符', trigger: 'blur' }
					],
					username: [
						{ required: true, message: '请输入用户名', trigger: 'blur' },
						{ min: 4, max: 15, message: '长度在 4 到 15 个字符', trigger: 'blur' }
					],
					pipe: [
						{ required: true, message: '请选择用户所属机构', trigger: 'change' }
					],
					phone: [
						{ max: 20, message: '最长为20个字符', trigger: 'blur' }
					]
				},
				editForm: {},
				addForm: {
					nickname: '',
					username: '',
					pipe: [],
					pass: '',
					checkPass: '',
					phone: '',
					address: '',
					remark: ''
				}
	  	}
	  },
	  created () {
	  	this._getIndex()
	  	this._getMsgList()
	  },
	  methods: {
	  	_getIndex (tip, url) {
	  		tip = urls.user.userIndex.tips
	  		url = urls.user.userIndex.url
	  		getData(tip, url).then((res) => {
          if (res.code === ERR_OK) {
            this.options = formatList(res.data.options)
          }
        })
	  	},
	  	_getMsgList (tip, url) {
	  		this.loadOn.tableLoading = true
	  		tip = urls.user.userList.tips
	  		url = urls.user.userList.url
	  		const data = Object.assign({}, tip, this.filters)

	  		getData(data, url).then((res) => {
          if (res.code === ERR_OK) {
            this.msgList = res.data.msg.data
            this.total = res.data.msg.total
          }
          console.log(this.msgList)
          this.loadOn.tableLoading = false
          this.loadOn.resetLoad = false
          this.loadOn.searchLoad = false
          this.loadOn.refreshLoad = false
        })
	  	},
	  	searchBtn () {
	  		this.loadOn.searchLoad = true
	  		this._getMsgList()
	  	},
	  	selectReset () {
	  		this.loadOn.resetLoad = true
	  		this.filters.optFilters = []
	  		this._getMsgList()
	  	},
	  	refreshPage () {
	  		this.loadOn.refreshLoad = true
	  		setTimeout(() => {
	  			this.loadOn.refreshLoad = false
	  		}, 2000)
	  		this._getMsgList()
	  		this._getIndex()
	  		this.loadOn.addFormVisible = false
        this.loadOn.editFormVisible = false
        this.loadOn.editLoading = false
        this.loadOn.addLoading = false
        this.loadOn.searchLoad = false
        this.loadOn.resetLoad = false
        this.loadOn.refreshLoa = false
	  	},
	  	sortChange (val) {
	  		if (val.prop !== null && val.order !== null) {
	  			this.filters.sortName = val.prop
	  			this.filters.orderType = val.order
	  		} else {
	  			this.filters.sortName = ''
	  			this.filters.orderType = ''
	  		}
	  		this._getMsgList()
	  	},
	  	handleSizeChange (val) {
        this.filters.pageSize = val
        this._getMsgList()
      },
      handleCurrentChange (val) {
        this.filters.currentPage = val
        this._getMsgList()
      },
      selectChange (val) {
      	this.delList = val
      	val.sort(comparePipe('pipe_id'))
      	console.log(val)
      },
      handleDel (row) {
		  	this.$confirm(`确认删除机构：${row.name} ？`, '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.user.userDel.tips
		  		let url = urls.user.userDel.url
		  		const data = Object.assign({}, tip, {
		  			'delList': [{'pipe_id': row.pipe_id}]
		  		})
          sendData(data, url).then((res) => {
          	let msg = ''
          	let type = ''
	          if (res.code === ERR_OK && res.data.err_ok === 1) {
	          	msg = '删除成功！'
	          	type = 'success'
	          	this._getMsgList()
	  					this._getIndex()
	          } else {
	          	msg = '删除失败！'
	          	type = 'error'
	          }
	          msgNotice(msg, type, false, true, this)
	        })
        })
      },
      handleDels () {
      	this.$confirm('只有根节点最后一级机构才能删除，是否继续？', '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.user.userDel.tips
		  		let url = urls.user.userDel.url
		  		const data = Object.assign({}, tip, {
		  			'delList': this.delList
		  		})
          sendData(data, url).then((res) => {
          	let msg = ''
          	let type = ''
	          if (res.code === ERR_OK) {
	          	msg = '删除成功！'
	          	type = 'success'
	          	this._getMsgList()
	  					this._getIndex()
	          } else if (res.code === 2) {
	          	type = ''
	          	msg = `<span style="color:green">${res.data.err_ok}</span> 个删除成功，<span style="color: red">${res.data.err}</span> 个删除失败。`
	          	if (res.data.err_ok !== 0) {
	          		this._getMsgList()
	  						this._getIndex()
	          	}
	          } else {
	          	type = 'error'
	          	msg = '发生错误，请刷新页面重试！'
	          }
	          msgNotice(msg, type, true, true, this)
	        })
        })
			},
			handleAdd () {
				this.loadOn.addFormVisible = true
			},
			addSubmit (formName) {
				this.$refs[formName].validate((valid) => {
          if (valid) {
            this.loadOn.addLoading = true
            let tip = urls.user.userAdd.tips
            let url = urls.user.userAdd.url
            const data = Object.assign({}, tip, this.addForm)
            sendData(data, url).then((res) => {
	          if (res.code === ERR_OK) {
				        msgNotice('添加成功！', 'success', false, true, this)
		          	this._getMsgList()
		  					this._getIndex()
		          }
		          this.loadOn.addLoading = false
		        }).catch(() => {
		        	this.loadOn.addLoading = false
		        	msgNotice('发生错误，请刷新页面重试！', 'error', false, false, this)
		        })
					} else {
            msgNotice('请按照规则填写带<span style="color: red"> * </span>号的选项与选填选项！', 'warning', true, true, this)
            return false
          }
        })
			},
			handleEdit (row) {
				this.loadOn.editFormVisible = true
				let len = this.options[0].value.length
				let pipe = []
				for (let i = 0; i < (row.pipe_id.length - len) / 4; i++) {
					pipe.push(row.pipe_id.slice(0, len + i * 4))
				}
				this.editForm = Object.assign({'pipe': pipe}, row)
			},
			editSubmit () {
				if (this.editForm.name.length !== 0 && this.editForm.pipe.length !== 0) {
					this.loadOn.editLoading = true
					let tip = urls.user.userEdit.tips
					let url = urls.user.userEdit.url
					const data = Object.assign({}, tip, this.editForm)
					sendData(data, url).then((res) => {
						if (res.code === ERR_OK) {
							msgNotice('编辑成功！', 'success', false, true, this)
							this._getMsgList()
	  					this._getIndex()
						} else if (res.code === 4) {
							msgNotice('无效操作！', '', false, true, this)
						} else if (res.code === 3) {
							msgNotice('不能选择当前机构作为父级机构！', 'warning', false, true, this)
						} else if (res.code === 2) {
							msgNotice('只有根节点最后一级机构才能更换父级机构！', 'warning', false, true, this)
						} else {
							msgNotice('发生错误，请刷新页面重试！', 'error', false, false, this)
						}
						this.loadOn.editLoading = false
					}).catch(() => {
	        	this.loadOn.editLoading = false
	        	msgNotice('发生错误，请刷新页面重试！', 'error', false, false, this)
	        })
				} else {
					msgNotice('带<span style="color: red"> * </span>号的选项不能为空！', 'warning', true, true, this)
					return false
				}
			}
	  },
	  components: {
	  	Crumb
	  }
	}
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
		
</style>