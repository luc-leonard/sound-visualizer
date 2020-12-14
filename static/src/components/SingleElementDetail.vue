<template>
  <div :class="$style.element">
    <youtube :class="$style.player"
             :video-id="get_youtube_id()"
             ref="youtube"
             :player-vars="players_vars"
             @paused="onPause"
             @playing="playing">
    </youtube>
    <div>{{ fps }}</div>
    <ScrollingCanvas :image_url="make_url(API_BASE_URL)"
                     width="2000"
                     :height="element.result.height / 4"
                     :tile_width="element.result.tile_width"
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
import ScrollingCanvas from "@/components/ScrollingCanvas.vue";


var getYouTubeID = require('get-youtube-id');
@Component({
  components: {ScrollingCanvas}
})
export default class SingleElementDetail extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;
  players_vars = {origin: window.location}
  player_start_time: number = 0;
  current_time_when_starting_to_play = 0;
  current_position = 0;
  pixel_per_sec: GLint64 = -1;
  youtube_player!: any
  is_playing: boolean = false;
  spectro!: ScrollingCanvas;

  mounted() {
    console.log(this);
    this.spectro = this.$refs.spectro as ScrollingCanvas;
    this.current_position = 0;
    // we multiply by 1000 because we want a fix point number to avoid propagating rounding errors.
    this.pixel_per_sec = (this.element.result.width / this.element.duration) * 1000;
    this.spectro.scrollTo(0);
  }

  async playing() {
    console.log('play')
    this.is_playing = true;
    this.current_time_when_starting_to_play = performance.now();
    await this.player().getCurrentTime().then((current_time: any) => {
      this.player_start_time = current_time * 1000;
    })
    requestAnimationFrame(this.update_position)
  }

  onPause() {
    console.log('pause')
    this.is_playing = false;
  }

  last_called_time = 0;
  fps: number = 0;

  async update_position(current_time: number) {
    let delta = (current_time - this.last_called_time) / 1000;
    this.last_called_time = current_time;
    this.fps = 1 / delta;

    if (this.is_playing) {
      let elapsed_time = current_time - this.current_time_when_starting_to_play;
      this.current_position = (elapsed_time + this.player_start_time) / 1000
      this.spectro.scrollTo((this.current_position * (this.pixel_per_sec / 1000)));
      requestAnimationFrame(this.update_position)
    }

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
.map {
  height: 510px;
}

.player {
  border: 1px solid yellow;
}

.image_container {
  overflow: scroll;
  width: 95%;
  border: 1px solid #ff0000;
  background-color: black;
}
</style>1