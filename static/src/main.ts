import Vue from 'vue'
import App from './App.vue'
import VueYoutube from 'vue-youtube'
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';


Vue.config.productionTip = false
Vue.use(VueYoutube)
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
let app = new Vue({
  render: h => h(App),
}).$mount('#app')

console.log(app)