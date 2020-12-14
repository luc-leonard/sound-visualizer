<template>
  <div :class="$style.element">
    <div>{{element.parameters.youtube_url}}</div>
    <div v-if="element.status == 'finished'">
      <ScrollingCanvas :image_url="make_url(API_BASE_URL)"
                       width="200"
                       :height="50"
                       :tile_width="element.result.tile_width"
                       :tile_height="element.result.height"
                       class="image_container"
                       :image_url_base="make_url(API_BASE_URL)"
                       ref="spectro"></ScrollingCanvas>
      </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import ScrollingCanvas from "@/components/ScrollingCanvas.vue";

@Component({
  components: {ScrollingCanvas}
})
export default class SingleElement extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;

  mounted() {
    let spectro = this.$refs.spectro as ScrollingCanvas;
    spectro.scrollTo(0);
  }


  make_url(base_url: string) {
    return base_url + '/tiles/' + this.element.id + '/'
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