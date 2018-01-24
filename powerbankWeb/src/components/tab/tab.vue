<template>
  <el-main class='tab-h'>
  	<el-tabs v-model="editableTabsValue" @tab-remove="removeTab" type="card">
		  <el-tab-pane
		    v-for="(item, index) in tabList"
		    :key="item.name"
		    :label="item.label"
		    :name="item.name"
		    :closable="item.closable"
		  >
        <component :is="item.component"></component>
		  </el-tab-pane>
		</el-tabs>
  </el-main>
</template>
<script>
  import {mapState, mapMutations} from 'vuex'

  export default {
    computed: {
      editableTabsValue: {
        get () {
          return this.activate
        },
        set (val) {
          this.setActive(val)
        }
      },
      ...mapState([
        'tabList',
        'activate'
      ])
    },
    methods: {
      removeTab (targetName) {
        let newtabList = this.tabList.slice()
        let tab = this.tabList.filter(f => f.name === targetName)[0]
        let index = newtabList.indexOf(tab)
        if (this.activate === targetName) {
          if (index !== newtabList.length - 1) {
            this.setActive(newtabList[index + 1].name)
          } else {
            this.setActive(newtabList[index - 1].name)
          }
        }
        this.changeTab(newtabList.filter(f => f.name !== targetName))
      },
      ...mapMutations({
        setActive: 'TURN_TO',
        changeTab: 'ADD_TAB'
      })
    }
  }
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
  .tab-h
    padding: 0
    >>> .el-tabs__header
      margin: 0  
</style>

