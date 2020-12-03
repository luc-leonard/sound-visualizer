<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <SpectralAnalysisFlowList :element-list="info"></SpectralAnalysisFlowList>
  </div>
</template>

<script lang="ts">

import Axios from "axios";
import {Component, Vue} from 'vue-property-decorator';
import SpectralAnalysisFlowList from "@/components/result_list/SpectralAnalysisFlowList.vue";
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
Vue.mixin({
  data() {
    return {
     //get API_BASE_URL() { return 'https://luc-leonard-sound-visualizer.herokuapp.com'}
     get API_BASE_URL() { return 'http://localhost:5000'}
    }
  }
})

@Component({
  components: {
    SpectralAnalysisFlowList,
  },
})

export default class App extends Vue {
  info: Array<SpectralAnalysisFlow> = [];
  mounted() {

    Axios
        .get(this.$data.API_BASE_URL + '/requests/?length=1')
        .then(response => {
              this.info = response.data
            }
        )

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
