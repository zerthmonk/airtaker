<template>
  <div class="photo-contain">
    <div class="user-photo"
        :style=photo>
    </div>
  </div>
</template>

<script>
const userUnknown = '/assets/user-unknown.jpg';

export default {
  props: {
    url: {
      type: String,
      default: userUnknown
    }
  },

  computed: {
    photo() { return `background-image: url(${this.url});` }
  }
}
</script>

<style lang="scss">
@import '../styles/variables';

  .photo-contain {
    width: 100%;
    background: $bg-darker;
    border: 2px solid darken($bg-light, 30%);
  }

  .user-photo {
    width: 100%;
    padding-bottom: 150%;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }

</style>
