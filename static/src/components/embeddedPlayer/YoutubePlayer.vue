<template>
  <div>
  <youtube
           :video-id="get_youtube_id()"
           ref="youtube"
           :player-vars="players_vars"
           @paused="onPause"
           @playing="playing">
  </youtube>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {Component, Prop} from "vue-property-decorator";

var getYouTubeID = require('get-youtube-id');

@Component({})
export default class MyYoutubePlayer extends Vue {
  @Prop({required: true})
  private url!: string;

  players_vars = {origin: window.location}
  youtube_player!: any


  get_youtube_id() {
    return getYouTubeID(this.url);
  }

  getCurrentTime() {
    return this.player().getCurrentTime();
  }

  player() {
    if (!this.youtube_player) {
      let youtube: any = this.$refs.youtube;
      this.youtube_player = youtube.player;
    }
    return this.youtube_player;
  }

  async playing() {
    this.$emit('playing', {})
  }

  onPause() {
    this.$emit('paused', {})
  }
}
</script>

<style scoped>

</style>