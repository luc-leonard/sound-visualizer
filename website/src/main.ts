import Vue from 'vue'
import App from './App.vue'
import VueYoutube from 'vue-youtube'
import router from "@/router";

Vue.config.productionTip = false
Vue.use(VueYoutube)


let app = new Vue({
  render: h => h(App),
  router
}).$mount('#app')

