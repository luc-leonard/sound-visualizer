<template>
  <div id="app">

    <router-view/>
    <router-link to="/">Home</router-link> -
    <router-link to="/about">About</router-link>
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
