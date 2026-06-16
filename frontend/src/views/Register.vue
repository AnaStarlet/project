<template>
  <div class="container">
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Имя пользователя" />
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <button type="submit">Зарегистрироваться</button>
    </form>
    <div class="links">
      Уже есть аккаунт?
      <a href="#" @click.prevent="$emit('switch-to-login')">Войти</a>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  emits: ['switch-to-login'],
  data() {
    return {
      username: '',
      email: '',
      password: '',
    }
  },
  methods: {
    async register() {
      try {
        await api.post('/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        })
        alert('Регистрация успешна! Теперь войдите.')
        this.$emit('switch-to-login')
      } catch (error) {
        console.error('Ошибка:', error.response?.data)
        alert('Ошибка регистрации: ' + (error.response?.data?.detail || 'неизвестная ошибка'))
      }
    },
  },
}

</script>