<template>
  <div class="new-spectral-form container">
    <div class="mb-5 gx-1">
      <form>
        <div class="">
          <span class="form-label">URL</span>
          <input type="text" class="form-control" v-model="url"/>
        </div>
        <div class="row">
          <div class="col-md-6">
            <span class="form-label">frame size</span>
            <input class="form-control" v-model="frame_size"/>
          </div>
          <div class="col-md-6">
            <span class="form-label">overlap factor</span>
            <input class="form-control" v-model="overlap_factor"/>
          </div>
        </div>
        <button @click="compute" class="btn btn-primary">COMPUTE</button>
<!--        <div class="card">{{ compute_result }}</div>-->
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import Axios from "axios";

@Component({
  components: {}
})

export default class NewSpectralForm extends Vue {
  url: String = 'https://youtube.com/...';
  frame_size: number = 12;
  overlap_factor: number = 0.8;

  current_result_id!: String;
  compute_result: String = "";

  compute() {
    console.log(this);
    Axios
        .post(process.env.VUE_APP_BASE_API_URL + '/requests/', {
          'youtube_url': this.url,
          'frame_size_power': this.frame_size,
          'overlap_factor': this.overlap_factor
        })
        .then(response => {
              this.current_result_id = response.data.id;
              this.poll_result()
            }
        )
  }

  poll_result() {
    setTimeout(() => {
      Axios.get(process.env.VUE_APP_BASE_API_URL + '/request/' + this.current_result_id)
          .then((response) => {
            if (response.data.status == 'finished') {
              this.$emit('finished', {'new_result': response.data})
            } else {
              this.compute_result = JSON.stringify(response.data);
              this.poll_result();
            }
          })
    }, 150)
  }
}
</script>

<style scoped>

</style>