<template>
  <div class="container">
    <div class="row d-flex">
      <div class="col align-self-center">
        <h1>LAST SPECTROGRAMS</h1>
      </div>
    </div>
    <div v-for="(elements, idx) in groupedElements()" class="row" :key="idx">
      <div v-for="element in elements" :key="element.id" class="col-sm-5 m-1">
          <SingleElement :element="element" @click="onClick"></SingleElement>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import SingleElement from "@/components/result_list/SingleElement.vue";
var _ = require('lodash')

@Component({
  components: {SingleElement}
})



export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private elementList!: Array<SpectralAnalysisFlow>;

  groupedElements() {
    return _.chunk(this.elementList, 2)
  }
  onClick(element: SpectralAnalysisFlow) {
    this.$emit('click', element)
  }
}
</script>


<style scoped>
ul {
  list-style: None;
}
li {

}
</style>