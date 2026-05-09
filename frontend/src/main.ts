import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles.css'
import { Form, Field, CellGroup } from 'vant';

const app = createApp(App)

app.use(createPinia())
app.use(router)

// VantUi 注入
app.use(Form);
app.use(Field);
app.use(CellGroup);

app.mount('#app')
