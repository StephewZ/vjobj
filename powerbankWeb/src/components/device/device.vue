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
					<el-button type="danger" size="mini" @click="handleDels" :disabled="this.delList.length===0 || this.loadOn.tableLoading">批量删除</el-button>
		  		<el-button size="mini" @click="handleAdd" :disabled="this.loadOn.tableLoading">添加</el-button>
	  		</el-button-group>
  		</el-col>
  		<el-col :span="10">
  			<el-button-group>
				  <el-button type="success" size="mini" icon="el-icon-upload">导入</el-button>
				  <el-button type="" size="mini" style="color:#409EFF">导出<i class="el-icon-download el-icon--right"></i></el-button>
				</el-button-group>
			</el-col=>
			<el-col :span="10" style="text-align: right">
				<el-button type="success" round size="mini" @click="refreshPage" :loading="refreshLoad"><i class="el-icon-refresh el-icon--left"></i>刷新</el-button>
			</el-col>
		</el-col>

		<el-table :data="msgList" highlight-current-row v-loading="loadOn.tableLoading" @sort-change="sortChange" @selection-change="selectChange">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column type="index" prop="pipe_id">
			</el-table-column>
			<el-table-column prop="device_num" label="设备编号">
			</el-table-column>
			<el-table-column prop="name" label="别名">
			</el-table-column>
			<el-table-column prop="parent" label="所属机构">
			</el-table-column>
			<el-table-column prop="creator" label="创建用户">
			</el-table-column>
			<el-table-column prop="remark" label="描述">
			</el-table-column>
			<el-table-column prop="made_time" label="添加时间" sortable="custom">
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
		<el-dialog title="添加设备" :visible.sync="loadOn.addFormVisible" :close-on-click-modal="true">
			<el-form :model="addForm" label-width="80px" :rules="FormRules" ref="addForm">
				<el-form-item label="设备编号" prop="device_num">
					<el-input  v-model="addForm.device_num" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="设备别称" prop="name">
					<el-input  v-model="addForm.name" auto-complete="off" maxlength="25" minlength="1"></el-input>
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
				<el-form-item label="绑定货道" prop="goods_pipe">
					<el-transfer
				    v-model="addForm.goods_pipe"
				    filterable
				    :titles="['货道列表', '绑定列表']"
				    :button-texts="['解绑', '绑定']"
				    :format="{
				      noChecked: '${total}',
				      hasChecked: '${checked}/${total}'
				    }"
				    @change="handleGoodsPipeChange"
				    :data="goods_pipeList">
				  </el-transfer>
				</el-form-item>
				<el-form-item label="设备描述" prop="remark">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="addForm.remark"
					  placeholder="设备描述">
					</el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="loadOn.addFormVisible = false" size="small">取消</el-button>
				<el-button type="primary" @click="addSubmit('addForm')" :loading="loadOn.addLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

	  <!--编辑界面-->
		<el-dialog title="设备编辑" :visible.sync="loadOn.editFormVisible" :close-on-click-modal="true">
			<el-form :model="editForm" label-width="80px" :rules="FormRules" ref="editForm">
				<el-form-item label="设备编号" prop="name">
					<el-input  v-model="editForm.device_num" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="设备别称" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
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

				<el-form-item label="绑定货道" prop="goods_pipe">
					<el-transfer
				    v-model="editForm.goods_pipe"
				    filterable
				    :titles="['货道列表', '绑定列表']"
				    :button-texts="['解绑', '绑定']"
				    :format="{
				      noChecked: '${total}',
				      hasChecked: '${checked}/${total}'
				    }"
				    @change="handleGoodsPipeChangeEdit"
				    :data="goods_pipeList">
				  </el-transfer>
				</el-form-item>

				<el-form-item label="设备描述" prop="remark">
					<el-input
					  type="textarea"
					  :rows="2"
					  maxlength="100"
					  v-model="editForm.remark"
					  placeholder="设备描述">
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
	import {formatList, formatGoodsPipeList, msgNotice} from 'common/js/dom'

	export default {
	  name: 'group',
	  data () {
	  	return {
	  		crumbMsg: ['产品管理', '设备管理'],
	  		filters: {
	  			'optFilters': [],
	  			'pageSize': 10,
	  			'currentPage': 1,
	  			'sortName': '',
	  			'orderType': '',
	  			'mixing': ''
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
	  		goods_pipeList: [],
        FormRules: {
        	device_num: [
						{ required: true, message: '请输入设备编号', trigger: 'blur' }
					],
					name: [
						{ required: true, message: '请输入设备别称', trigger: 'blur' }
					],
					pipe: [
						{ required: true, message: '请选择上级机构', trigger: 'change' }
					]
				},
				editForm: {},
				addForm: {
					device_num: '',
					goods_pipe: [],
					name: '',
					pipe: [],
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
	  		tip = urls.device.deviceIndex.tips
	  		url = urls.device.deviceIndex.url
	  		getData(tip, url).then((res) => {
          if (res.code === ERR_OK) {
            this.options = formatList(res.data.options)
            this.goods_pipeList = formatGoodsPipeList(res.data.goods_pipeList)
          }
        })
	  	},
	  	_getMsgList (tip, url) {
	  		this.loadOn.tableLoading = true
	  		tip = urls.device.deviceList.tips
	  		url = urls.device.deviceList.url
	  		const data = Object.assign({}, tip, this.filters)

	  		getData(data, url).then((res) => {
          if (res.code === ERR_OK) {
            this.msgList = res.data.msg.data
            this.total = res.data.msg.total
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
	  		this.filters.mixing = ''
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
	  	handleGoodsPipeChange () {
	  		console.log('1')
	  		let k = 0
  			for (let j = 0; j < this.goods_pipeList.length; j++) {
  				this.goods_pipeList[j]['label'] = '* - ' + this.goods_pipeList[j]['label'].substr(this.goods_pipeList[j]['label'].indexOf(' - ') + 3)
  			}
  			for (let i = 0; i < this.addForm.goods_pipe.length; i++) {
  				for (let j = 0; j < this.goods_pipeList.length; j++) {
  					if (this.addForm.goods_pipe[i] === this.goods_pipeList[j]['key']) {
  						k++
  						this.goods_pipeList[j]['label'] = k + ' - ' + this.goods_pipeList[j]['label'].substr(this.goods_pipeList[j]['label'].indexOf(' - ') + 3)
  					}
  				}
  			}
	  	},
	  	handleGoodsPipeChangeEdit () {
	  		console.log('2')
	  		let k = 0
  			for (let j = 0; j < this.goods_pipeList.length; j++) {
  				this.goods_pipeList[j]['label'] = '* - ' + this.goods_pipeList[j]['label'].substr(this.goods_pipeList[j]['label'].indexOf(' - ') + 3)
  			}
  			for (let i = 0; i < this.editForm.goods_pipe.length; i++) {
  				for (let j = 0; j < this.goods_pipeList.length; j++) {
  					if (this.editForm.goods_pipe[i] === this.goods_pipeList[j]['key']) {
  						k++
  						this.goods_pipeList[j]['label'] = k + ' - ' + this.goods_pipeList[j]['label'].substr(this.goods_pipeList[j]['label'].indexOf(' - ') + 3)
  					}
  				}
  			}
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
		  	this.$confirm(`确认删除设备：${row.device_num} ？`, '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.device.deviceDel.tips
		  		let url = urls.device.deviceDel.url
		  		const data = Object.assign({}, tip, {
		  			'delList': [{'device_num': row.device_num, 'id': row.id}]
		  		})
          sendData(data, url).then((res) => {
          	let msg = ''
          	let type = ''
	          if (res.code === ERR_OK && res.data.err_ok === 1) {
	          	msg = '删除成功！'
	          	type = 'success'
	          	this._getMsgList()
	  					this._getIndex()
	          } else if (res.code === 404) {
	          	type = 'warning'
	          	msg = '删除失败: 无权限！'
	          } else if (res.code === 2) {
	          	msg = '删除失败: 设备不存在！'
	          	type = 'error'
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
      	this.$confirm('只有根节点最后一级机构才能删除，是否继续？', '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.inst.instDel.tips
		  		let url = urls.inst.instDel.url
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
	          } else if (res.code === 404) {
	          	type = 'warning'
	          	msg = '删除失败: 无权限！'
	          } else {
	          	msg = '删除失败！'
	          	type = 'error'
	          }
	          msgNotice(msg, type, true, true, this)
	        })
        }).catch(() => {
        	return false
        })
			},
			handleAdd () {
				this.loadOn.addFormVisible = true
				this.handleGoodsPipeChange()
			},
			addSubmit (formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.loadOn.addLoading = true
						let tip = urls.device.deviceAdd.tips
						let url = urls.device.deviceAdd.url
						const data = Object.assign({}, tip, this.addForm)
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
		          } else if (res.code === 2) {
		          	type = 'warning'
		          	msg = '添加失败: 设备已存在！'
		          } else if (res.code === 3) {
		          	type = 'warning'
		          	msg = '添加失败: 设备编号不正确，请核对后重新添加！'
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
						msgNotice('带<span style="color: red"> * </span>号的选项不能为空！', 'warning', true, true, this)
						return false
					}
				})
			},
			handleEdit (row) {
				this.loadOn.editFormVisible = true
				let len = this.options[0].value.length
				let pipe = []
				for (let i = 0; i < (row.pipe_id.length - len) / 4 + 1; i++) {
					pipe.push(row.pipe_id.slice(0, len + i * 4))
				}
				this.editForm = Object.assign({'pipe': pipe}, row)
				this.handleGoodsPipeChangeEdit()
			},
			editSubmit (formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.loadOn.editLoading = true
						let tip = urls.device.deviceEdit.tips
						let url = urls.device.deviceEdit.url
						const data = Object.assign({}, tip, this.editForm)
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
		          	type = '发生错误，请刷新页面重试！'
		          	msg = 'error'
							}
							msgNotice(msg, type, false, true, this)
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
		// >>> .el-dialog
		// 	width: 60%
</style>