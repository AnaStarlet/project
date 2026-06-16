<template>
  <div id="app">
    <Login v-if="page === 'login'" @switch-to-register="page = 'register'" />
    <Register v-else-if="page === 'register'" @switch-to-login="page = 'login'" />
    <Notes v-else />
  </div>
</template>

<script>
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Notes from './views/Notes.vue'

export default {
  components: { Login, Register, Notes },
  data() {
    return {
      page: 'login',
    }
  },
  mounted() {
    const token = localStorage.getItem('access_token')
    if (token) {
      this.page = 'notes'
    }
  },
}
</script>

<style>
@import './style.css';
</style>