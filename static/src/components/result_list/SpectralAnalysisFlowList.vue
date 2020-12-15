<template>
  <ul>
    <li v-for="element in elementList" :key="element.id">
      <div v-if="element.status == 'finished'">
        <SingleElement :element="element" @click="onClick"></SingleElement>
        </div>
    </li>
  </ul>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SingleElement from "@/components/result_list/SingleElement.vue";
@Component({
  components: {SingleElement}
})
export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private elementList!: Array<SpectralAnalysisFlow>;

  onClick(element: SpectralAnalysisFlow) {
    this.$emit('click', element)
  }
}
</script>


<style scoped>

</style>