<template>
  <div class="message">
    <h1>GENERATOR</h1>
    <div v-on:click="generate">{{value}}</div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import {RandomStringGenerator} from '@/model/RandomStringGenerator'


@Component
export default class RandomStringComponent extends Vue {
  @Prop({default: 420})
  private seed!: number;

  private value: string = 'CLICK ME';

  public generate(){
    let generator = new RandomStringGenerator(this.seed);
    this.value = generator.generateRandomString()
  }
}

</script>

<style scoped>

</style>