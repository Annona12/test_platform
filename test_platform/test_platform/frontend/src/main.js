import { createApp } from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
createApp.use(ElementUI);

createApp(App).mount('#app')
