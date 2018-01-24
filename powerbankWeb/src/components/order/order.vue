<template>
  <div>
		<crumb :crumbMsg="crumbMsg"></crumb>
		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="设备编号"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="mini" v-on:click="">查询</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="mini" @click="">重置</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<el-col :span="24" class="toolbar">
			<el-button-group>
				<el-button type="danger" size="mini" @click="" :disabled="this.deviceList.length===0">批量删除</el-button>
	  		<el-button size="mini" @click="">添加</el-button>
  		</el-button-group>
		</el-col>

		<el-table :data="deviceList" highlight-current-row v-loading="tableLoading">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column type="index">
			</el-table-column>
			<el-table-column prop="name" label="姓名">
			</el-table-column>
			<el-table-column prop="age" label="年龄" sortable>
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
	      :current-page="currentPage"
	      :page-sizes="[10, 20, 40, 10000]"
	      :page-size="100"
	      layout="total, sizes, prev, pager, next, jumper"
	      :total="total">
	    </el-pagination>
	  </div>

	  <!--编辑界面-->
		<el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="true">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="设备编号" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="设备状态">
					<el-radio-group v-model="editForm.name">
						<el-radio class="radio" :label="1">在线</el-radio>
						<el-radio class="radio" :label="0">离线</el-radio>
					</el-radio-group>
				</el-form-item>
				<el-form-item label="年龄">
					<el-input-number v-model="editForm.age" :min="0" :max="200"></el-input-number>
				</el-form-item>
				<el-form-item label="地址">
					<el-input type="textarea" v-model="editForm.age"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

  </div>
</template>
<script>
	import Crumb from 'components/crumb/crumb'

	export default {
	  name: 'device',
	  data () {
	  	return {
	  		filters: {
	  			name: ''
	  		},
	  		crumbMsg: ['数据分析', '订单记录'],
	  		tableLoading: false,
        currentPage: 1,
        total: 0,
        deviceList: [{'name': '11', 'age': 111}, {'name': '22', 'age': 222}],
        editFormVisible: false,
        editLoading: false,
        editFormRules: {
					name: [
						{ required: true, message: '请输入姓名', trigger: 'blur' }
					]
				},
				editForm: {
					id: 0
				}
	  	}
	  },
	  methods: {
	  	handleSizeChange (val) {
        console.log(`每页 ${val} 条`)
      },
      handleCurrentChange (val) {
        console.log(`当前页: ${val}`)
      },
      handleDel: function (row) {
		  	console.log(row)
			},
			handleEdit: function (row) {
				this.editFormVisible = true
				this.editForm = Object.assign({}, row)
				console.log(this.editFormVisible)
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
	.el-table
		width: 100%
		min-height: 540px
	.block .el-pagination
		text-align: center
		padding: 10px 0
</style>