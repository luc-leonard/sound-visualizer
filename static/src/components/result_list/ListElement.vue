<template>
  <div class="element">
    <youtube :video-id="get_youtube_id()" ref="youtube"
             :player-vars="players_vars" @playing="playing"></youtube>
    <div>{{ current_position }}</div>
    <button @click="update_position"/>
    <div class="image" ref="image_container">
      <img alt="spectrogram" :src="make_url(API_BASE_URL)" ref="image"/>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";

var getYouTubeID = require('get-youtube-id');

@Component
export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;
  players_vars = {origin: window.location}
  current_position: number = 0;
  pixel_per_sec = -1;
  youtube_player!: any

  playing(){
    console.log("START PLAYING")
    this.$nextTick(function () {
            window.setInterval(() => {
                this.update_position();
            },25);
        })
  }
  update_position() {
    if (this.pixel_per_sec == -1) {
      let image: any = this.$refs.image;
      this.player().getDuration().then((duration: number) => this.pixel_per_sec = image.width / duration)
    }

    this.player().getCurrentTime().then((current_time: any) => {
      let container: any = this.$refs.image_container;
      this.current_position = current_time;
      container.scrollTo(current_time * this.pixel_per_sec, 0);
    })
  }

  get_youtube_id() {
    return getYouTubeID(this.element.parameters.youtube_url)
  }

  make_url(base_url: string) {
    return base_url + '/result/' + this.element.id
  }

  player() {
    if (!this.youtube_player) {
      let youtube: any = this.$refs.youtube;
      this.youtube_player = youtube.player;
    }
    return this.youtube_player;
  }
}
</script>

<style scoped>
.image {
  overflow: auto;
  width: 1000px;
}
</style>1