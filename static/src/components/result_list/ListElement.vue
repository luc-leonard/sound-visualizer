<template>
  <div class="element">
    <h3>{{element.parameters.url}}</h3>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";


@Component
export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private element!: SpectralAnalysisFlow;
}
</script>

<style scoped>

</style>