<template>
  <div class="new-spectral-form">
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">URL</span>
      <input type="text" class="form-control" v-model="url"/>
    </div>
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">frame size</span>
      <input class="form-control" v-model="frame_size"/>
    </div>
    <div class="input-group">
      <span class="input-group-addon" id="basic-addon1">overlap factor</span>
      <input class="form-control" v-model="overlap_factor"/>
    </div>
    <button @click="compute">COMPUTE</button>

    <div class="well">{{ compute_result }}</div>
  </div>
</template>

<script lang="ts">
import {Vue, Component} from "vue-property-decorator";
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
      Axios.get(process.env.VUE_APP_BASE_API_URL + '/result/' + this.current_result_id)
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