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
					<el-button type="danger" size="mini" @click="handleDels" :disabled="this.delList.length===0 || this.loadOn.tableLoading">批量删除</el-button>
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
			<el-table-column type="index" prop="id">
			</el-table-column>
			<el-table-column prop="name" label="角色名称">
			</el-table-column>
			<el-table-column prop="parent" label="所属机构">
			</el-table-column>
			<el-table-column prop="is_enabled" label="状态">
			</el-table-column>
			<el-table-column prop="creator" label="创建用户">
			</el-table-column>
			<el-table-column prop="remark" label="描述">
			</el-table-column>
			<el-table-column prop="made_time" label="创建时间" sortable="custom">
			</el-table-column>
			<el-table-column prop="edit_time" label="最近编辑" sortable="custom">
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
		<el-dialog title="添加角色" :visible.sync="loadOn.addFormVisible" :close-on-click-modal="true">
			<el-form :model="addForm" ref="addForm" label-width="80px" :rules="FormRules">
				<el-form-item label="角色名称" prop="name">
					<el-input  v-model="addForm.name" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="是否启用" prop="is_enabled">
					<el-switch
					  v-model="addForm.is_enabled"
					  active-color="#13ce66"
					  inactive-color="#c0c4cc"
					  active-value="启用"
    				inactive-value="禁用">
					</el-switch>
				</el-form-item>
				<el-form-item label="角色类型" prop="status_type">
					<el-radio-group v-model="addForm.status_type">
				    <el-radio :label="1">下级机构可编辑</el-radio>
				    <el-radio :label="0">下级机构不可编辑</el-radio>
				  </el-radio-group>
				</el-form-item>
				<el-form-item label="权限配置">
					<el-tree
					  :data="data3"
					  show-checkbox
					  node-key="id"
					  ref="addTree"
					  :default-checked-keys="['0.001', '0.002', '0.003']">
					</el-tree>
				</el-form-item>
				<el-form-item label="描述" prop="remark">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="addForm.remark"
					  placeholder="描述">
					</el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="loadOn.addFormVisible = false" size="small">取消</el-button>
				<el-button type="primary" @click="addSubmit('addForm')" :loading="loadOn.addLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

	  <!--编辑界面-->
		<el-dialog title="角色编辑" :visible.sync="loadOn.editFormVisible" :close-on-click-modal="true">
			<el-form :model="editForm" label-width="80px" :rules="FormRules" ref="editForm">
				<el-form-item label="角色名称" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="是否启用" prop="is_enabled">
					<el-switch
					  v-model="editForm.is_enabled"
					  active-color="#13ce66"
					  inactive-color="#c0c4cc"
					  active-value="启用"
    				inactive-value="禁用">
					</el-switch>
				</el-form-item>
				<el-form-item label="角色类型" prop="status_type">
					<el-radio-group v-model="editForm.status_type">
				    <el-radio :label="1">下级机构可编辑</el-radio>
				    <el-radio :label="0">下级机构不可编辑</el-radio>
				  </el-radio-group>
				</el-form-item>
				<el-form-item label="权限配置">
					<el-tree
					  :data="data3"
					  show-checkbox
					  node-key="id"
					  ref="editTree">
					</el-tree>
				</el-form-item>
				<el-form-item label="角色描述" prop="remark">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="editForm.remark"
					  placeholder="角色描述">
					</el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="loadOn.editFormVisible = false" size="small">取消</el-button>
				<el-button type="primary" @click="editSubmit('editForm')" :loading="loadOn.editLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

  </div>
</template>
<script>
	import Crumb from 'components/crumb/crumb'
	import {getData, sendData} from 'api/data'
	import {urls, ERR_OK} from 'api/config'
	import {formatList, msgNotice, formatPowerList} from 'common/js/dom'

	export default {
	  name: 'group',
	  data () {
	  	return {
	  		data1: [],
	  		data3: [],
	  		crumbMsg: ['管理员管理', '角色管理'],
	  		filters: {
	  			'optFilters': [],
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
					name: [
						{ required: true, message: '请输入机构名称', trigger: 'blur' }
					],
					is_enabled: [
						{ required: true }
					],
					status_type: [
						{ required: true }
					]
				},
				editForm: {},
				addForm: {
					name: '',
					is_enabled: '启用',
					status_type: 1,
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
	  		tip = urls.status.statusIndex.tips
	  		url = urls.status.statusIndex.url
	  		getData(tip, url).then((res) => {
          if (res.code === ERR_OK) {
            this.options = formatList(res.data.options)
          }
        })
	  	},
	  	_getMsgList (tip, url) {
	  		this.loadOn.tableLoading = true
	  		tip = urls.status.statusList.tips
	  		url = urls.status.statusList.url
	  		const data = Object.assign({}, tip, this.filters)

	  		getData(data, url).then((res) => {
          if (res.code === ERR_OK) {
            this.msgList = res.data.msg.data
            this.total = res.data.msg.total
            this.data1 = formatPowerList(res.data.plist, res.data.permitList)
          }
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
      },
      handleDel (row) {
		  	this.$confirm('角色关联的用户将无法正常使用，是否继续？', '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.status.statusDel.tips
		  		let url = urls.status.statusDel.url
		  		const data = Object.assign({}, tip, {
		  			'delList': [{'id': row.id}]
		  		})
          sendData(data, url).then((res) => {
          	let msg = ''
          	let type = ''
	          if (res.code === ERR_OK) {
	          	msg = '删除成功！'
	          	type = 'success'
	          	this._getMsgList()
	  					this._getIndex()
	          } else if (res.code === 404) {
	          	type = 'warning'
	          	msg = '删除失败: 无权限！'
	          } else {
	          	msg = '删除失败！'
	          	type = 'error'
	          }
	          msgNotice(msg, type, false, true, this)
	        })
        }).catch(() => {
        	return false
        })
      },
      handleDels () {
      	this.$confirm('角色关联的用户将无法正常使用，是否继续？', '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.status.statusDel.tips
		  		let url = urls.status.statusDel.url
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
	          } else if (res.code === 404) {
	          	type = 'warning'
	          	msg = '删除失败: 无权限！'
	          } else {
	          	type = 'error'
	          	msg = '发生错误，请刷新页面重试！'
	          }
	          msgNotice(msg, type, false, true, this)
	        })
        }).catch(() => {
        	return false
        })
			},
			handleAdd () {
				this.data3 = this.data1
				this.loadOn.addFormVisible = true
			},
			addSubmit (formName) {
				this.$refs[formName].validate((valid) => {
          if (valid) {
            this.loadOn.addLoading = true
            let tip = urls.status.statusAdd.tips
            let url = urls.status.statusAdd.url
            const data = Object.assign({'powers': this.$refs.addTree.getCheckedKeys()}, tip, this.addForm)
            sendData(data, url).then((res) => {
	          let msg = ''
          	let type = ''
	          if (res.code === ERR_OK) {
	          	msg = '添加成功！'
	          	type = 'success'
	          	this._getMsgList()
	  					this._getIndex()
	          } else if (res.code === 404) {
	          	type = 'warning'
	          	msg = '添加失败: 无权限！'
	          } else {
	          	type = 'error'
	          	msg = '发生错误，请刷新页面重试！'
	          }
	          msgNotice(msg, type, true, true, this)
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
				this.data3 = this.data1
				this.loadOn.editFormVisible = true
				this.editForm = Object.assign({}, row)
				setTimeout(() => {
					this.$refs.editTree.setCheckedKeys(row.powerlist)
				}, 20)
			},
			editSubmit (formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.loadOn.editLoading = true
						let tip = urls.status.statusEdit.tips
						let url = urls.status.statusEdit.url
						const data = Object.assign({'powers': this.$refs.editTree.getCheckedKeys()}, tip, this.editForm)
						sendData(data, url).then((res) => {
							let msg = ''
	          	let type = ''
		          if (res.code === ERR_OK) {
		          	msg = '编辑成功！'
		          	type = 'success'
		          	this._getMsgList()
		  					this._getIndex()
		          } else if (res.code === 404) {
		          	type = 'warning'
		          	msg = '编辑失败: 无权限！'
		          } else {
		          	type = 'error'
		          	msg = '发生错误，请刷新页面重试！'
		          }
		          msgNotice(msg, type, true, true, this)
							this.loadOn.editLoading = false
						}).catch(() => {
		        	this.loadOn.editLoading = false
		        	msgNotice('发生错误，请刷新页面重试！', 'error', false, false, this)
		        })
					} else {
						msgNotice('带<span style="color: red"> * </span>号的选项不能为空！', 'warning', true, true, this)
						return false
					}
				})
			}
	  },
	  components: {
	  	Crumb
	  }
	}
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
		
</style>