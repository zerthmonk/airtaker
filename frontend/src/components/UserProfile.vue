<template>
  <div class="user-profile">
    <div class="column is-one-third">
      <user-photo :url=photoUrl></user-photo>
    </div>
    <div class="column is-two-third">
      <user-name :name=nameData></user-name>
      <user-methods :methods=methodsData></user-methods>
    </div>
  </div>
</template>

<script>
import UserMethods from './UserMethods.vue';
import UserName from './UserName.vue';
import UserPhoto from './UserPhoto.vue';

export default {
  // Component naming is not so abstract.
  // Trying to KISS and stay in scope of test application.
  components: {
    UserMethods,
    UserName,
    UserPhoto,
  },

  props: {
    user: {
      type: Object
    }
  },

  computed: {
    nameData() { return this.user.name },
    methodsData() { return this.user.methods },
    photoUrl() { return this.user.photo }
  }
}
</script>

<style lang="scss">
  .user-profile {
    height: 100%;
    display: flex;
  }
</style>
