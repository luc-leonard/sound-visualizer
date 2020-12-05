<template>
    <div :class="$style.image_container">

      <canvas ref="theCanvas" :class="$style.spectrogram"></canvas>
    </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({})
export default class ScrollingCanvas extends Vue {
  @Prop({required: true})
  image_url!: string;
  @Prop({required: true})
  width!: number;
  @Prop({required: true})
  height!: number;
  image!: HTMLImageElement;
  context!: CanvasRenderingContext2D;
  mounted() {
    console.log('loading image...')
    this.image = new Image(this.width, this.height);
    let canvas = (this.$refs.theCanvas as any);
    this.context = canvas.getContext('2d')
    canvas.width = 1000;
    canvas.height = 2000;
    this.image.onload = () => {
      this.scrollTo(0)

    }
    this.image.src = this.image_url;
  }

  private drawLineAt(x: number) {
    this.context.moveTo(x, 0)
    this.context.lineTo(x, 2000)
    this.context.strokeStyle = 'red';
    this.context.stroke()
  }
  // eslint-disable-next-line no-unused-vars
  scrollTo(x: number) {
     this.context.drawImage(this.image, -x + 500, -this.height / 2);
     this.drawLineAt(500);
  }
}
</script>

<style module>
.image_container {
  border: 1px solid blue;
  height: 1900px;
  width: 90%;
}

.spectrogram {
  border: 1px solid red;
  height: 100%;
  width: 100%;
}

</style>