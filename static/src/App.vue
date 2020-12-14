<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">URL</span>
      <input type="text" class="form-control" v-model="value"/>
    </div>
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">frame size</span>
      <input class="form-control" v-model="frame_size"/>
    </div>
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">overlap factor</span>
      <input class="form-control" v-model="overlap_factor"/>
    </div>
    <button @click="compute"> COMPUTE</button>

    <div class="well">{{compute_result}}</div>
    <div v-if="info[0] != null">
      <SingleElementDetail :element="info[0]"></SingleElementDetail>
    </div>
    <SpectralAnalysisFlowList :element-list="info"></SpectralAnalysisFlowList>
  </div>
</template>

<script lang="ts">

import Axios from "axios";
import {Component, Vue} from 'vue-property-decorator';
import SingleElementDetail from "@/components/SingleElementDetail.vue";
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SpectralAnalysisFlowList from "@/components/result_list/SpectralAnalysisFlowList.vue";

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
    SingleElementDetail,
  },
})

export default class App extends Vue {
  info: Array<SpectralAnalysisFlow> = []
  value: String = "https://youtu.be/ZS8o9EpwUHg"
  compute_result: String = "";
  current_result_id: String = "";
  frame_size: Number = 12;
  overlap_factor: Number = 0.9;

  compute() {
    Axios
        .post(this.$data.API_BASE_URL + '/requests/', {
          'youtube_url': this.value,
          'frame_size_power': this.frame_size,
          'overlap_factor': this.overlap_factor
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
        .get(this.$data.API_BASE_URL + '/requests/')
        .then(response => {
              this.info = response.data;
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
