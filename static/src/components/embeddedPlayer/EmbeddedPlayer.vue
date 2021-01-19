<template>
  <div>
    <MyYoutubePlayer
        ref="player"
        :url="element.parameters.youtube_url"
        @playing="$emit('playing')"
        @paused="$emit('paused')"
        v-if="isYoutube()"
    ></MyYoutubePlayer>
    <SoundcloudPlayer
        v-else
        ref="player"
        :url="element.parameters.youtube_url"
        @seek="$emit('seek')"
        @playing="$emit('playing')"
        @paused="$emit('paused')">
    </SoundcloudPlayer>
  </div>
</template>

<script lang="ts">

import Vue from "vue";
import {Component, Prop} from "vue-property-decorator";
import MyYoutubePlayer from "@/components/embeddedPlayer/YoutubePlayer.vue";
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SoundcloudPlayer from "@/components/embeddedPlayer/SoundcloudPlayer.vue";


@Component({
  components: {SoundcloudPlayer, MyYoutubePlayer}
})


export default class EmbeddedPlayer extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;

  isYoutube() {
    return this.element.parameters.youtube_url.indexOf('youtube') > 0;
  }
  getCurrentTime() {
    return (this.$refs.player as MyYoutubePlayer).getCurrentTime();
  }
}
</script>

<style scoped>

</style>