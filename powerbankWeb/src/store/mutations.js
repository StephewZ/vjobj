import * as types from './mutation-types'

const mutations = {
  [types.TURN_TO] (state, aim) {
    state.activate = aim
  },
  [types.ADD_TAB] (state, tab) {
    state.tabList = tab
  }
}

export default mutations
