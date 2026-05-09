import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Vant from 'vant';
import 'vant/lib/index.css';
import './styles.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// VantUi 注入
app.use(Vant);

// Lazyload 指令需要单独进行注册
// app.use(vant.Lazyload);
app.mount('#app')
