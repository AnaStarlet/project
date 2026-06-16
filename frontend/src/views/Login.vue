<template>
  <div class="container">
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Имя пользователя" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <button type="submit">Войти</button>
    </form>
    <div class="links">
      Нет аккаунта?
      <a href="#" @click.prevent="$emit('switch-to-register')">Зарегистрироваться</a>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  emits: ['switch-to-register'],
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    async login() {
      try {
        const formData = new URLSearchParams()
        formData.append('username', this.username)
        formData.append('password', this.password)

        const response = await api.post('/auth/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })

        localStorage.setItem('access_token', response.data.access_token)
        this.$parent.page = 'notes'
      } catch (error) {
        console.error('Ошибка:', error.response?.data)
        alert('Ошибка входа: ' + (error.response?.data?.detail || 'неверные данные'))
      }
    },
  },
}
</script>