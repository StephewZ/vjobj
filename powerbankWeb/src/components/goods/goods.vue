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
			<el-table-column
	      label="商品信息">
	      <template slot-scope="scope">
	        <el-popover trigger="hover" placement="top">
	          <p>商品名称: {{ scope.row.name }}</p>
	          <p>描述: {{ scope.row.remark }}</p>
	          <p>创建用户: {{ scope.row.creator }}</p>
	          <div slot="reference" class="name-wrapper">
	            <el-tag size="medium">{{ scope.row.name }}</el-tag>
	          </div>
	        </el-popover>
	      </template>
	    </el-table-column>
	    <el-table-column prop="goods_num" label="商品编号">
			</el-table-column>
			<el-table-column prop="purchase_price" label="成本" sortable="custom">
			</el-table-column>
			<el-table-column prop="retail_price" label="售价" sortable="custom">
			</el-table-column>
			<el-table-column prop="parent" label="所属机构">
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
		<el-dialog title="添加商品" :visible.sync="loadOn.addFormVisible" :close-on-click-modal="true">
			<el-form :model="addForm" label-width="80px" :rules="FormRules" ref="addForm">
				<el-form-item label="商品编号" prop="goods_num">
					<el-input  v-model="addForm.goods_num" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="商品名称" prop="name">
					<el-input  v-model="addForm.name" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>

				<el-form-item label="商品成本" prop="purchase_price">
					<el-input  v-model="addForm.purchase_price" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="商品售价" prop="retail_price">
					<el-input  v-model="addForm.retail_price" auto-complete="off" maxlength="25" minlength="1"></el-input>
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
		<el-dialog title="商品编辑" :visible.sync="loadOn.editFormVisible" :close-on-click-modal="true">
			<el-form :model="editForm" label-width="80px" :rules="FormRules" ref="editForm">
				<el-form-item label="商品编号" prop="name">
					<el-input  v-model="editForm.goods_num" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>

				<el-form-item label="商品名称" prop="name">
					<el-input  v-model="editForm.name" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="商品成本" prop="purchase_price">
					<el-input  v-model="editForm.purchase_price" auto-complete="off" maxlength="25" minlength="1"></el-input>
				</el-form-item>
				<el-form-item label="商品售价" prop="retail_price">
					<el-input  v-model="editForm.retail_price" auto-complete="off" maxlength="25" minlength="1"></el-input>
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
				<el-button type="primary" @click="editSubmit('editForm')" :loading="loadOn.editLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

  </div>
</template>
<script>
	import Crumb from 'components/crumb/crumb'
	import {getData, sendData} from 'api/data'
	import {urls, ERR_OK} from 'api/config'
	import {formatList, msgNotice} from 'common/js/dom'
	import {mul} from 'common/js/arit'

	export default {
	  name: 'group',
	  data () {
	  	let validatePrice = (rule, value, callback) => {
        if (/^\d+(\.\d+)?$/.test(+value) === false) {
          callback(new Error('请输入数字'))
        } else if (('' + value).split('.').length === 2) {
        	if (('' + value).split('.')[1].length > 2) {
        		callback(new Error('只能输入两位小数'))
        	} else {
        		callback()
        	}
        } else {
        	callback()
        }
      }
	  	return {
	  		crumbMsg: ['产品管理', '商品管理'],
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
        FormRules: {
        	goods_num: [
						{ required: true, message: '请输入商品编号', trigger: 'blur' },
						{ min: 1, max: 25, message: '长度在 1 到 25 个字符', trigger: 'blur' }
					],
					name: [
						{ required: true, message: '请输入商品名称', trigger: 'blur' },
						{ min: 1, max: 25, message: '长度在 1 到 25 个字符', trigger: 'blur' }
					],
					purchase_price: [
						{ required: true, validator: validatePrice, trigger: 'blur' },
						{ min: 1, max: 25, trigger: 'blur' }
					],
					retail_price: [
						{ required: true, validator: validatePrice, trigger: 'blur' },
						{ min: 1, max: 25, trigger: 'blur' }
					],
					pipe: [
						{ required: true, message: '请选择上级机构', trigger: 'change' }
					]
				},
				editForm: {},
				addForm: {
					goods_num: '',
					name: '',
					purchase_price: '',
					retail_price: '',
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
	  		tip = urls.goods.goodsIndex.tips
	  		url = urls.goods.goodsIndex.url
	  		getData(tip, url).then((res) => {
          if (res.code === ERR_OK) {
            this.options = formatList(res.data.options)
          }
        })
	  	},
	  	_getMsgList (tip, url) {
	  		this.loadOn.tableLoading = true
	  		tip = urls.goods.goodsList.tips
	  		url = urls.goods.goodsList.url
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
		  	this.$confirm(`确认删除商品：${row.name} ？`, '提示', {type: 'warning'}).then(() => {
		  		let tip = urls.goods.goodsDel.tips
		  		let url = urls.goods.goodsDel.url
		  		const data = Object.assign({}, tip, {
		  			'delList': [{'goods_num': row.goods_num, 'id': row.id}]
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
	          	msg = '删除失败: 商品使用中，请先删除商品对应的货道！'
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
      	this.$confirm('货道正在使用的商品无法删除，是否继续？', '提示', {type: 'warning'}).then(() => {
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
			},
			addSubmit (formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.loadOn.addLoading = true
						let tip = urls.goods.goodsAdd.tips
						let url = urls.goods.goodsAdd.url
						const data = Object.assign({
							'p_price': mul(this.addForm.purchase_price, 100),
							'r_price': mul(this.addForm.retail_price, 100)
						}, tip, this.addForm)
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
		          	msg = '添加失败: 商品编号重复！'
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
			},
			editSubmit (formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.loadOn.editLoading = true
						let tip = urls.goods.goodsEdit.tips
						let url = urls.goods.goodsEdit.url
						const data = Object.assign({
							'p_price': mul(this.editForm.purchase_price, 100),
							'r_price': mul(this.editForm.retail_price, 100)
						}, tip, this.editForm)
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
		          } else if (res.code === 2) {
		          	type = 'warning'
		          	msg = '编辑失败：商品编号重复，机构已存在该商品编号！'
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
		
</style>