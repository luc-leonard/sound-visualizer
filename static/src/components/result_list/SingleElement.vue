<template>
  <div :class="$style.element" >
    <h2 @click="$emit('click', element)"><a>{{element.title}}</a></h2>
    <img :src="thumbnail_url()" :alt="element.parameters.youtube_url"/>
    <div v-if="element.status == 'finished'">
      <img :src="first_tile_url()" :class="$style.spectro">
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
    return this.make_url(process.env.VUE_APP_BASE_API_URL) +  '/0.png'
  }

  make_url(base_url: string) {
    return base_url + '/tiles/' + this.element.id + '/'
  }

}
</script>

<style module>
.spectro {
  width: 90%;
  height: 250px;
  object-fit: scale-down;
}
</style>1