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

  images = new Array<HTMLImageElement | null>();
  context!: CanvasRenderingContext2D;
  private loadingImages = new Map<number, boolean>();

  mounted() {
    let canvas = this.$refs.theCanvas as any;
    canvas.width = this.width;
    canvas.height = this.height;

    this.context = canvas.getContext('2d')

    this.scrollTo(0)
  }

  private drawLineAt(x: number) {
    this.context.moveTo(x, 0)
    this.context.lineTo(x, this.height)
    this.context.strokeStyle = 'red';
    this.context.stroke()
  }

  clear() {
    this.loadingImages.clear();
    this.images = [];
  }
  // eslint-disable-next-line no-unused-vars
  scrollTo(x: number) {
    let first_image_to_show = Math.floor(x / this.tile_width)
    let last_image_to_show = Math.floor((x + this.context.canvas.width) / this.tile_width)

    for (let i = first_image_to_show; i <= last_image_to_show; ++i) {
      if (this.images[i] == null && !this.loadingImages.has(i)) {
        this.loadingImages.set(i, false);
        this.getImage(i).then(image => {
          this.images[i] = image;
          this.loadingImages.set(i, true);
          this.scrollTo(x);
        });
      }
    }

    if (this.loadingImages.get(first_image_to_show) == true) {
        this.context.drawImage(this.images[first_image_to_show]!,
          -(x % this.tile_width) + this.width / 2, this.height - this.tile_height);
    }
    this.drawLineAt(this.width / 2);
  }


  private async getImage(x: number) {
    console.log("loading tile", x);
    return new Promise<HTMLImageElement>((resolve, reject) => {
      let img = new Image()
      img.onload = () => {
        console.log('loaded tile ', x)
        resolve(img)
      }
      img.onerror = reject
      img.src = this.image_url_base + x + '.png'
    })

  }
}
</script>

<style module>
.image_container {
  border: 1px solid blue;
  width: 90%;
}

.spectrogram {
  border: 1px solid red;
  height: 100%;
  width: 100%;
}

</style>