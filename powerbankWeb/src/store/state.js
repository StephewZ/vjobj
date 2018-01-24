const Home = (resolve) => {
  import('components/home/home').then((module) => {
    resolve(module)
  })
}

const state = {
  activate: 'home',
  tabList: [
    {
      label: '主页',
      name: 'home',
      closable: false,
      component: Home
    }
  ]
}

export default state
