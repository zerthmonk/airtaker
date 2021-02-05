<template>
  <div class="profile-heading">
    <p>{{name}}</p>
  </div>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
    }
  }
}
</script>

<style lang="scss">
@import '../styles/variables';

  .profile-heading {
    font-size: 2rem;
    text-transform: capitalize;
    background-color: $bg-darker;
    padding: 8px;

    p {
      margin: 0;
      text-align: center;
    }
  }

</style>
