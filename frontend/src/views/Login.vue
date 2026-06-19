<template>
  <div class="container">
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Имя пользователя" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Вход...' : 'Войти' }}
      </button>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
    
    <div class="links">
      <div>
        Нет аккаунта?
        <router-link to="/register">Зарегистрироваться</router-link>
      </div>
      <div style="margin-top: 8px;">
        <router-link to="/reset-password">Забыли пароль?</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  methods: {
    async login() {
      this.loading = true
      this.error = ''
      
      try {
        const formData = new URLSearchParams()
        formData.append('username', this.username)
        formData.append('password', this.password)

        const response = await api.post('/auth/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })

        localStorage.setItem('access_token', response.data.access_token)
        this.router.push('/notes')
      } catch (error) {
        const detail = error.response?.data?.detail
        if (detail === 'Please verify your email first') {
          this.error = 'Пожалуйста, подтвердите ваш email. Проверьте почту.'
        } else {
          this.error = 'Ошибка входа: ' + (detail || 'неверные данные')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.error-message {
  color: #e53e3e;
  text-align: center;
  font-size: 14px;
  margin-top: -5px;
}
</style>