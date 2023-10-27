import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// import Axios from 'axios'


const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router)
app.mount('#app')
// createApp.prototype.$axios = Axios
// Axios.defaults.baseURL = '/api'