<template>
  <div class="card">
    <div class="card-header" @click="$emit('click', element)">
      <a href="#">{{ element.title }}</a>
    </div>
    <div class="card-body">
      <img :src="thumbnail_url()" :alt="element.parameters.youtube_url"/>
      <div>
        <img :src="first_tile_url()" :class="$style.spectro" height="150">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import ScrollingCanvas from "@/components/result_detail/ScrollingCanvas.vue";

var getYouTubeID = require('get-youtube-id');

@Component({
  components: {ScrollingCanvas}
})
export default class SingleElement extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;

  thumbnail_url() {
    let video_id = getYouTubeID(this.element.parameters.youtube_url)
    return 'https://img.youtube.com/vi/' + video_id + '/0.jpg';
  }

  first_tile_url() {
    return this.make_url(process.env.VUE_APP_BASE_API_URL) + '/0.png'
  }

  make_url(base_url: string) {
    return base_url + '/tiles/' + this.element.id + '/'
  }

}
</script>

<style module>
h2 {
  height: 50px;
}

a {
  cursor: pointer;
}

.spectro {
  width: 90%;
  height: 250px;
  object-fit: scale-down;
}
</style>1