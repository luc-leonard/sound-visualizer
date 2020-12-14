<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <input type="text" id="youtube_url" v-model="value"/>
    <button @click="compute"> COMPUTE</button>
    <br />
    <textarea v-model="compute_result"></textarea>
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
      //get API_BASE_URL() { return 'https://sound-visualizer-staging.herokuapp.com'}
      //get API_BASE_URL() { return 'https://luc-leonard-sound-visualizer.herokuapp.com'}
      get API_BASE_URL() {
        let params = new URLSearchParams(window.location.search.substring(1));
        return params.get('api_url');
      }
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
  value: String = "test"
  compute_result: String = "";
  current_result_id: String = "";

  compute() {
    Axios
        .post(this.$data.API_BASE_URL + '/requests/', {
          'youtube_url': this.value,
          'frame_size_power': 12,
          'overlap_factor': 0.9
        })
        .then(response => {
              this.current_result_id = response.data.id;
              this.poll_result()
            }
        )
  }

  poll_result() {
    setTimeout(() => {
      Axios.get(this.$data.API_BASE_URL + '/result/' + this.current_result_id)
          .then((response) => {
            if (response.data.status == 'finished') {
              this.info = [response.data];
            } else {
              this.compute_result = JSON.stringify(response.data);
              this.poll_result();
            }
          })
    }, 150)
  }

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
