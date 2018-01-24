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
					<el-button type="danger" size="mini" @click="" :disabled="this.msgList.length===0 || this.loadOn.tableLoading">批量删除</el-button>
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

		<el-table :data="msgList" highlight-current-row v-loading="loadOn.tableLoading" @sort-change="sortChange">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column type="index" prop="pipe_id">
			</el-table-column>
			<el-table-column prop="name" label="机构名称">
			</el-table-column>
			<el-table-column prop="parent" label="上级机构">
			</el-table-column>
			<el-table-column prop="creator" label="创建用户">
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
	      :page-sizes="[10, 25, 50, 100]"
	      :page-size="filters.pageSize"
	      layout="total, sizes, prev, pager, next, jumper"
	      :total="total">
	    </el-pagination>
	  </div>

	  <!--添加界面-->
		<el-dialog title="添加机构" :visible.sync="loadOn.addFormVisible" :close-on-click-modal="true">
			<el-form label-width="80px" :rules="addFormRules" ref="addForm">
				<el-form-item label="机构名称" prop="name">
					<el-input  auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="上级机构" prop="parent">
					<el-cascader
				    placeholder="请选择机构"
				    :options="options"
				    filterable
				    change-on-select
				  ></el-cascader>
				</el-form-item>
				<el-form-item label="年龄">
					<el-input-number :min="0" :max="200"></el-input-number>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="loadOn.addFormVisible = false" size="small">取消</el-button>
				<el-button type="primary" @click="addSubmit" :loading="loadOn.addLoading" size="small">提交</el-button>
			</div>
		</el-dialog>

	  <!--编辑界面-->
		<el-dialog title="机构编辑" :visible.sync="loadOn.editFormVisible" :close-on-click-modal="true">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="机构名称" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="上级机构" prop="parent">
					<el-cascader
				    placeholder="请选择机构"
				    :options="options"
				    filterable
				    v-model="editForm.pipe_id"
				    change-on-select
				  ></el-cascader>
				</el-form-item>
				<el-form-item label="年龄">
					<el-input-number v-model="editForm.age" :min="0" :max="200"></el-input-number>
				</el-form-item>
				<el-form-item label="地址">
					<el-input type="textarea" v-model="editForm.age"></el-input>
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
	import {getData} from 'api/data'
	import {urls, ERR_OK} from 'api/config'
	import {formatList} from 'common/js/math'

	export default {
	  name: 'group',
	  data () {
	  	return {
	  		crumbMsg: ['产品管理', '机构管理'],
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
	  		options: [{
          value: 'ziyuan',
          label: '资源',
          children: [{
            value: 'axure',
            label: 'Axure Components'
          }, {
            value: 'sketch',
            label: 'Sketch Templates'
          }, {
            value: 'jiaohu',
            label: '组件交互文档'
          }]
        }],
        addFormRules: {
					name: [
						{ required: true, message: '请输入姓名', trigger: 'blur' }
					]
				},
        editFormRules: {
					name: [
						{ required: true, message: '请输入姓名', trigger: 'blur' }
					]
				},
				editForm: {}
	  	}
	  },
	  created () {
	  	this._getIndex()
	  	this._getMsgList()
	  },
	  methods: {
	  	_getIndex (tip, url) {
	  		tip = urls.inst.instIndex.tips
	  		url = urls.inst.instIndex.url
	  		getData(tip, url).then((res) => {
          if (res.code === ERR_OK) {
            this.options = formatList(res.data.options)
          }
        })
	  	},
	  	_getMsgList (tip, url) {
	  		this.loadOn.tableLoading = true
	  		tip = urls.inst.instList.tips
	  		url = urls.inst.instList.url
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
	  		this._getMsgList()
	  	},
	  	refreshPage () {
	  		this.loadOn.refreshLoad = true
	  		setTimeout(() => {
	  			this.loadOn.refreshLoad = false
	  		}, 2000)
	  		this._getMsgList()
	  		this._getIndex()
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
        console.log(`每页 ${val} 条`)
      },
      handleCurrentChange (val) {
        console.log(`当前页: ${val}`)
      },
      handleDel: function (row) {
		  	console.log(row)
			},
			handleAdd () {
				this.loadOn.addFormVisible = true
			},
			handleEdit (row) {
				this.loadOn.editFormVisible = true
				this.editForm = Object.assign({}, row)
				console.log(row)
			},
			addSubmit () {

			},
			editSubmit () {
				console.log(this.editForm)
			}
	  },
	  components: {
	  	Crumb
	  }
	}
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
		
</style>