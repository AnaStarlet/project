<template>
  <div class="container">
    <h2>Восстановление пароля</h2>
    
    <div v-if="step === 'request'">
      <p>Введите ваш email</p>
      <form @submit.prevent="requestReset">
        <input v-model="email" type="email" placeholder="Email" required />
        <button type="submit" :disabled="loading">Отправить</button>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">Письмо отправлено</div>
      </form>
      <div class="links">
        <router-link to="/login">Вернуться к входу</router-link>
      </div>
    </div>

    <div v-else-if="step === 'reset'">
      <h2>Сброс пароля</h2>
      <form @submit.prevent="resetPassword">
        <input v-model="newPassword" type="password" placeholder="Новый пароль" required minlength="6" />
        <input v-model="confirmPassword" type="password" placeholder="Подтвердите пароль" required minlength="6" />
        <button type="submit" :disabled="loading || newPassword !== confirmPassword || newPassword.length < 6">Сбросить пароль</button>
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>

    <div v-else-if="step === 'reset-success'">
      <h2>Пароль изменен</h2>
      <button @click="goToLogin">Войти</button>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'
import { useRouter, useRoute } from 'vue-router'

export default {
  data() {
    return {
      step: 'request',
      email: '',
      newPassword: '',
      confirmPassword: '',
      resetToken: '',
      loading: false,
      error: '',
      success: false
    }
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    return { router, route }
  },
  mounted() {
    this.checkToken()
  },
  methods: {
    checkToken() {
      const token = this.route.query.token
      if (token) {
        this.step = 'reset'
        this.resetToken = token
        console.log('Токен сброса получен:', token)
      }
    },
    async requestReset() {
      this.loading = true
      this.error = ''
      this.success = false
      try {
        await api.post('/auth/request-password-reset', null, {
          params: { email: this.email }
        })
        this.success = true
        this.email = ''
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка'
      } finally {
        this.loading = false
      }
    },
    async resetPassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.error = 'Пароли не совпадают'
        return
      }
      if (this.newPassword.length < 6) {
        this.error = 'Пароль должен быть не менее 6 символов'
        return
      }
      this.loading = true
      this.error = ''
      try {
        await api.post('/auth/reset-password', {
          token: this.resetToken,
          new_password: this.newPassword
        })
        this.step = 'reset-success'
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка сброса пароля'
      } finally {
        this.loading = false
      }
    },
    goToLogin() {
      this.router.push('/login')
    }
  },
  watch: {
    '$route.query.token'(newToken) {
      if (newToken) {
        this.step = 'reset'
        this.resetToken = newToken
        console.log('Токен сброса обновлён:', newToken)
      }
    }
  }
}
</script>

<style scoped>
.error {
  color: #e53e3e;
  text-align: center;
  margin-top: 10px;
}
.success {
  color: #27ae60;
  text-align: center;
  margin-top: 10px;
}
.links {
  text-align: center;
  margin-top: 16px;
}
.links a {
  color: #EE82EE;
  text-decoration: none;
}
</style>