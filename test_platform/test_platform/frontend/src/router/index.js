import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout'
import Login from '@/views/Login'
import Home from '@/views/Home'


const routes = [
  {
    path: '/',
    name: 'layout',
    component:Layout,
    children:[
    {
        path: '/',
        name: 'home',
        component: Home
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
