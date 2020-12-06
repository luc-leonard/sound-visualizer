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
  image_url_base!: string;
  @Prop({required: true})
  width!: number;
  @Prop({required: true})
  height!: number;
  @Prop({required: true})
  tile_width!: number;
  @Prop({required: true})
  tile_height!: number;

  images: Array<HTMLImageElement | null> = new Array<HTMLImageElement | null>();
  context!: CanvasRenderingContext2D;
  mounted() {
    console.log('loading image...')

    let canvas = (this.$refs.theCanvas as any);
    this.context = canvas.getContext('2d')
    canvas.width = this.width;
    canvas.height = this.height;
    console.log(this)
    this.scrollTo(0)
  }

  private drawLineAt(x: number) {
    this.context.moveTo(x, 0)
    this.context.lineTo(x, this.height)
    this.context.strokeStyle = 'red';
    this.context.stroke()
  }
  // eslint-disable-next-line no-unused-vars
  async scrollTo(x: number) {
    let first_image_to_show = Math.floor(x / this.tile_width)
    let last_image_to_show = Math.floor((x + this.context.canvas.width) / this.tile_width)
    for (let i = 0; i < first_image_to_show; ++i) {
      this.images[i] = null;
    }
    for (let i = first_image_to_show; i <= last_image_to_show; ++i) {
      if (this.images[i] == null) {
        this.images[i] = await this.getImage(i)
      }
    }
    this.context.drawImage(this.images[first_image_to_show]!,
        -(x % this.tile_width) + this.width / 2, 0);
    for (let i = first_image_to_show + 1; i <= last_image_to_show; ++i) {
      this.context.drawImage(this.images[i]!,
          -(x % this.tile_width) + (i * this.tile_width) + this.width / 2, 0);
    }
     //this.context.drawImage(this.image, -x + 500, - this.height / 2);
     this.drawLineAt(this.width / 2);
  }

  private async getImage(x: number) {
    console.log("loading tile", x);
    return new Promise<HTMLImageElement>((resolve, reject) => {
      let img = new Image()
      img.onload = () => {resolve(img)}
      img.onerror = reject
      img.src = this.image_url_base + x + '.png'
    })

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