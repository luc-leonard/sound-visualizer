<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <SpectralAnalysisFlowList :element-list="info"></SpectralAnalysisFlowList>
  </div>
</template>

<script lang="ts">

import Axios from "axios";
import {Component, Vue} from 'vue-property-decorator';
import HelloWorld from './components/HelloWorld.vue';
import RandomStringComponent from "@/components/RandomStringComponent.vue";
import SpectralAnalysisFlowList from "@/components/result_list/SpectralAnalysisFlowList.vue";
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";

@Component({
  components: {
    HelloWorld,
    RandomStringComponent,
    SpectralAnalysisFlowList,
  },
})

export default class App extends Vue {
  info: Array<SpectralAnalysisFlow> = [];

  mounted() {
    Axios
        .get('http://localhost:5000/requests')
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
