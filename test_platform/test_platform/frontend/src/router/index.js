import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout'
import Login from '@/views/Login'
import Home from '@/views/Home'
import Users from '@/views/Users'
import List from '@/views/Users/userlist'
import Info from '@/views/Users/userinfo'


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
    {
        path: '/users',
        name: 'users',
        component: Users,
        children:[
            {
                path:'list',
                name:'list',
                component:List
            },
             {
                path:'info',
                name:'info',
                component:Info
            },

        ]
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
      children: [

      ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
