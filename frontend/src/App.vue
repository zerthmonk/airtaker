<template>
  <div class="container">
    <div  v-if="userData.length">
      <user-profile
        v-for="(user, index) in userData"
        :key="index"
        :user="user"
        ></user-profile>
    </div>
    <p v-else>data loading...</p>
  </div>
</template>

<script>
import axios from 'axios';
import UserProfile from './components/UserProfile.vue';

// .env for JS not mastered still
const BACKEND_URL = 'http://127.0.0.1:8000/api';

export default {
  components: {
    UserProfile,
  },

  data() {
    return {
      userData: []
    }
  },

  mounted() {
    this.getData();
  },

  methods: {
    getData() {
      axios.get(`${BACKEND_URL}/profiles`)
        .then(response => {
          if (response.data.error) { throw response.data.error };
          this.userData = response.data.result;
        })
        .catch (errorMessage => {
          console.error(errorMessage);
        })
      },
  }
}
</script>

<style lang="scss">
// CSS frameworks not mentioned in task description, so all styles are home-made :)
@import 'styles/variables';

html, body {
  padding: 0;
  margin: 0;
  color: $main-color;
  background-color: $bg-light;
}

.container {
  max-width: $max-width;
  margin: auto;
  padding: 24px 0;
}

.column {
  padding: 16px;
}

.is-one-third {
  width: 33%;
}

.is-two-third {
  width: 66%;
}

</style>
