<template>
  <div>
    <iframe width="100%" height="166" ref="soundcloud_iframe"
            :src="getFullURL()">
    </iframe>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {Component, Prop} from "vue-property-decorator";
// eslint-disable-next-line no-unused-vars


@Component({})
export default class SoundcloudPlayer extends Vue {
  @Prop({required: true})
  private url!: string;

  players_vars = {origin: window.location}
  youtube_player!: any
  widget!: any

  mounted() {
    let iframe = this.$refs.soundcloud_iframe as HTMLIFrameElement
    let SC = (window as any).SC
    this.widget = SC.Widget(iframe)
    console.log(this.widget);
    this.widget.bind(SC.Widget.Events.PLAY, () => this.$emit('playing'))
    this.widget.bind(SC.Widget.Events.PAUSE, () => this.$emit('paused'))
    this.widget.bind(SC.Widget.Events.SEEK, () => {
      this.$emit('seek');
    })
  }


  getCurrentTime() {
    let promise = new Promise((resolve, reject) => {
      this.widget.getPosition((position: number) => resolve(position / 1000))
      let b = true
      if (!b) {
        reject(null);
      }
    })
    return promise;
  }

  getFullURL() {
    return "https://w.soundcloud.com/player/?url=" + this.url
  }
}
</script>

<style scoped>

</style>