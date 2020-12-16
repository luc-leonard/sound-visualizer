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

  private images = new Array<HTMLImageElement | null>();
  private context!: CanvasRenderingContext2D;
  private loadingImages = new Map<number, boolean>();
  private canvas!: HTMLCanvasElement

  mounted() {
    let canvas = this.$refs.theCanvas as any;
    canvas.width = this.width;
    canvas.height = this.height;

    this.context = canvas.getContext('2d');
    this.canvas = canvas;
    this.scrollTo(0)
  }

  private drawLineAt(x: number) {
    this.context.moveTo(x, 0)
    this.context.lineTo(x, this.canvas.height)
    this.context.strokeStyle = 'red';
    this.context.stroke()
  }

  requestFullScreen() {
    let old_width = this.canvas.width;
    let old_height = this.canvas.height;
    this.canvas.style.width = window.innerWidth + "px";
    this.canvas.style.height = window.innerHeight + "px";
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.canvas.requestFullscreen({});
    this.canvas.addEventListener('fullscreenchange', () => {
      //means out of full screen. awful.
        if (document.fullscreenElement == null) {
          this.canvas.height = old_height;
          this.canvas.width = old_width;
          this.canvas.style.width = this.canvas.width + "px";
          this.canvas.style.height = this.canvas.height + "px";
        }
    })
  }

  clear() {
    this.loadingImages.clear();
    this.images = [];
  }
  // eslint-disable-next-line no-unused-vars
  scrollTo(x: number) {
    let first_image_to_show = Math.floor(x  / this.tile_width)
    let last_image_to_show = Math.floor((x + this.canvas.width) / this.tile_width)

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
         0,
          this.tile_height - this.canvas.height,
          this.tile_width,
          this.canvas.height,
          -(x % this.tile_width) + this.canvas.width / 2,
            0,
          this.tile_width,
        this.canvas.height);
    }
    let j = 1;
    for (let i = first_image_to_show + 1; i <= last_image_to_show; i++) {
      if (this.loadingImages.get(i)) {
        this.context.drawImage(this.images[i]!,
            0,
            this.tile_height - this.canvas.height,
            this.tile_width,
            this.canvas.height,
            -(x % this.tile_width) + this.canvas.width / 2 + (j * this.tile_width),
            0,
            this.tile_width,
            this.canvas.height);
      }
      j++;
    }
    this.drawLineAt(this.canvas.width / 2);
  }


  private async getImage(x: number) {
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
  width: 100%;
}

.spectrogram {
  height: 100%;
  width: 100%;
}

</style>