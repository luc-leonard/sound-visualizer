<template>
  <div class="home">
    <h1>Last spectrograms</h1>
    <SpectralAnalysisFlowList :element-list="last_elements" @click="onClick"></SpectralAnalysisFlowList>
  </div>
</template>

<script lang="ts">

// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SpectralAnalysisFlowList from "@/components/result_list/SpectralAnalysisFlowList.vue"
import Vue from "vue";
import {Component} from "vue-property-decorator";
import Axios from "axios";

@Component({
  components: {
    SpectralAnalysisFlowList
  },
})
export default class extends Vue {
  last_elements: Array<SpectralAnalysisFlow> = []
  onClick(element: SpectralAnalysisFlow) {
    console.log(element)
    this.$router.push({name:'render', params:{'result_id': element.id}});
  }
  mounted() {
    Axios
        .get(process.env.VUE_APP_BASE_API_URL + '/requests/')
        .then(response => {
              this.last_elements = response.data;
            }
        )
  }
}
</script>
