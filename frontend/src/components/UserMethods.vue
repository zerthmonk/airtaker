<template>
  <div class='user-methods'>
    <p class='user-methods__heading'>{{heading}}:</p>
    <div class="user-methods__contain">
      <div class="method" v-for="(item, index) in methods" :key="index">{{item}}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    methods: {
      type: Array,
    },
    heading: {
      type: String,
      default: 'Методы'
    }
  },
}
</script>

<style lang='scss'>
@import '../styles/variables.scss';

  .user-methods__heading {
    font-size: 1.5rem;
    padding-left: 8px;
  }

  .user-methods__contain {
    font-size: .875rem;
  }

  .method {
    float: left;
    margin-right: 1rem;
    margin-bottom: 1rem;
    padding: 8px 16px;
    background-color: $bg-darker;
    text-transform: uppercase;
  }

</style>
