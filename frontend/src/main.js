/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

window.django_host = 'http://127.0.0.1:8000' // TODO: Move to .env

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import {numberWithSpaces} from "@/filters/numberWithSpaces";

const app = createApp(App)

app.config.globalProperties.$filters = {
  numberWithSpaces
};

registerPlugins(app)

app.mount('#app')
