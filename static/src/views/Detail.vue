<template>
  <div class="home">
    <h1>Last spectrograms</h1>
    <button @click="close" type="button" class="close" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    <SingleElementDetail v-if="element != null" :element="element"></SingleElementDetail>
  </div>
</template>

<script lang="ts">

// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SingleElementDetail from "@/components/result_detail/SingleElementDetail.vue";
import Vue from "vue";
import {Component} from "vue-property-decorator";
import Axios from "axios";

@Component({
  components: {
    SingleElementDetail,
  },
})
export default class extends Vue {
  element:SpectralAnalysisFlow | null = null;
  close() {
    this.$router.push({path: '/'});
  }
  mounted() {
    console.log(this.$route);
        Axios
        .get(process.env.VUE_APP_BASE_API_URL + '/request/' + this.$route.params['result_id'])
        .then(response => {
              this.element = response.data;
            }
        )
  }
}
</script>
