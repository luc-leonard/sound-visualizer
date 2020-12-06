<template>
  <div :class="$style.element">
    <youtube :class="$style.player" :video-id="get_youtube_id()" ref="youtube" :player-vars="players_vars" @playing="playing">
    </youtube>
    <ScrollingCanvas :image_url="make_url(API_BASE_URL)"
                      width="2000"
                      :height="element.result.height"
                     tile_width="5000"
                     :tile_height="element.result.height"
                     class="image_container"
                     :image_url_base="make_url(API_BASE_URL)"
                     ref="spectro"></ScrollingCanvas>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import VueOpenSeaDragon from "@/components/ScrollingCanvas.vue";
import ScrollingCanvas from "@/components/ScrollingCanvas.vue";


var getYouTubeID = require('get-youtube-id');
@Component({
  components: {ScrollingCanvas, VueOpenSeaDragon}
})
export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;
  players_vars = {origin: window.location}
  current_position: number = 0;
  pixel_per_sec = -1;
  youtube_player!: any


  playing() {
    console.log("START PLAYING")
    this.$nextTick(function () {
      //requestAnimationFrame(this.update_position);
      window.setInterval(() => {
        this.update_position();
      }, 25);
    })
  }

  async update_position() {
    if (this.pixel_per_sec == -1) {
      this.player().getDuration().then((duration: number) => {
        this.pixel_per_sec =  this.element.result.width / duration;
      });
    }

    await this.player().getCurrentTime().then((current_time: any) => {
      let spectro: VueOpenSeaDragon = this.$refs.spectro as VueOpenSeaDragon;
      this.current_position = current_time;
      spectro.scrollTo(current_time * this.pixel_per_sec + 10);
    })
  }

  get_youtube_id() {
    return getYouTubeID(this.element.parameters.youtube_url)
  }

  make_url(base_url: string) {
    return base_url + '/tiles/' + this.element.id + '/'
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

<style module>
.map{
  height: 510px;
}

.player {
  border:1px solid yellow;
}
.image_container {
  overflow: scroll;
  width: 95%;
  border: 1px solid #ff0000;
  background-color: black;
}
</style>1