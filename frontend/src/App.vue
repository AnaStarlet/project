<template>
  <div id="app">
    <EmailVerification v-if="page === 'verify-email'" />
    <Login v-else-if="page === 'login'" @switch-to-register="page = 'register'" />
    <Register v-else-if="page === 'register'" @switch-to-login="page = 'login'" />
    <PasswordReset v-else-if="page === 'password-reset'" />
    <Notes v-else />
  </div>
</template>

<script>
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Notes from './views/Notes.vue'
import PasswordReset from './views/PasswordReset.vue'
import EmailVerification from './views/EmailVerification.vue'

export default {
  components: { Login, Register, Notes, PasswordReset, EmailVerification },
  data() {
    return {
      page: 'login',
    }
  },
  mounted() {
    const token = localStorage.getItem('access_token')
    const params = new URLSearchParams(window.location.search)
    if (params.get('token')) {
      this.page = 'verify-email'
    } else if (token) {
      this.page = 'notes'
    }
  },
}
</script>

<style>
@import './style.css';
</style>