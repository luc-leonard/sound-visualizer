<template>
  <ul>
    <li v-for="element in elementList" :key="element.id">
      {{ element }}
    </li>
  </ul>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";


@Component
export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private elementList!: Array<SpectralAnalysisFlow>;

}
</script>


<style scoped>

</style>