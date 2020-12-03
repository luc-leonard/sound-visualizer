<template>
  <ul>
    <li v-for="element in elementList" :key="element.id">
      <ListElement :element="element"></ListElement>
    </li>
  </ul>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
// eslint-disable-next-line no-unused-vars
import {SpectralAnalysisFlow} from "@/model/SpectralAnalysisFlow";
import ListElement from "@/components/result_list/ListElement.vue";
@Component({
  components: {ListElement}
})
export default class SpectralAlaysisFlowListElement extends Vue {
  @Prop({required: true})
  private elementList!: Array<SpectralAnalysisFlow>;

}
</script>


<style scoped>

</style>