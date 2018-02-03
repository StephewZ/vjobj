import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Focus = (resolve) => {
  import('components/focus/focus').then((module) => {
    resolve(module)
  })
}

const Pay = (resolve) => {
  import('components/pay/pay').then((module) => {
    resolve(module)
  })
}

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '*',
      redirect: '/focus'
    },
    {
      path: '/focus',
      name: 'Focus',
      component: Focus
    },
    {
      path: '/pay/:num',
      name: 'Pay',
      component: Pay
    }
  ]
})
