import { createApp } from 'vue'
import App from './App.vue'
// import ElementPlus from 'element-plus'
// import 'element-plus/dist/index.css'
import router from './router/index'
// createApp(App).use(router).mount('#app')
const app = createApp(App)
//
app.use(router)
// app.use(ElementPlus)
app.mount('#app')
// createApp.use(ElementPlus);
//
// createApp(App).mount('#app')
