<template>
  <div class="home">
    <h1>New Spectrogram ?</h1>
    <NewSpectralForm @finished="update_list"></NewSpectralForm>
    <SpectralAnalysisFlowList :element-list="last_elements" @click="onClick"></SpectralAnalysisFlowList>
  </div>
</template>

<script lang="ts">

// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SpectralAnalysisFlowList from "@/components/result_list/SpectralAnalysisFlowList.vue"
import NewSpectralForm from "@/components/NewSpectralForm.vue";
import Vue from "vue";
import {Component} from "vue-property-decorator";
import Axios from "axios";

@Component({
  components: {
    SpectralAnalysisFlowList,
    NewSpectralForm,
  },
})
export default class extends Vue {
  last_elements: Array<SpectralAnalysisFlow> = []

  onClick(element: SpectralAnalysisFlow) {
    console.log(element)
    this.$router.push({name: 'render', params: {'result_id': element.id}});
  }

  update_list() {
    Axios
        .get(process.env.VUE_APP_BASE_API_URL + '/requests/?status=finished&length=15')
        .then(response => {
              this.last_elements = response.data;
            }
        )
  }
  mounted() {
    this.update_list()
  }
}
</script>
