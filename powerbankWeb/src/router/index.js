import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Focus = (resolve) => {
  import('components/focus/focus').then((module) => {
    resolve(module)
  })
}

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/focus'
    },
    {
      path: '/focus',
      component: Focus
    }
  ]
})
