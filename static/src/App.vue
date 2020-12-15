<template>
  <div id="app">
    <img src="./assets/logo.png" alt="logo">
    <router-view/>
    <router-link to="/">Home</router-link> -
    <router-link to="about">About</router-link>
  </div>
</template>

<script lang="ts">

import {Component, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars



@Component({
  components: {
  },
})

export default class App extends Vue {
  api_url = process.env.VUE_APP_BASE_API_URL;
  // compute() {
  //   Axios
  //       .post(this.$data.API_BASE_URL + '/requests/', {
  //         'youtube_url': this.value,
  //         'frame_size_power': this.frame_size,
  //         'overlap_factor': this.overlap_factor
  //       })
  //       .then(response => {
  //             this.current_result_id = response.data.id;
  //             this.poll_result()
  //           }
  //       )
  // }
  //
  // poll_result() {
  //   setTimeout(() => {
  //     Axios.get(this.$data.API_BASE_URL + '/result/' + this.current_result_id)
  //         .then((response) => {
  //           if (response.data.status == 'finished') {
  //             this.info = [response.data];
  //           } else {
  //             this.compute_result = JSON.stringify(response.data);
  //             this.poll_result();
  //           }
  //         })
  //   }, 150)
  // }
  //
  mounted() {
    // Axios
    //     .get(this.$data.API_BASE_URL + '/requests/')
    //     .then(response => {
    //           this.info = response.data;
    //         }
    //     )
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
