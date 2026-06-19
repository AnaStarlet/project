<template>
  <div class="container">
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Имя пользователя" required minlength="3" />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Пароль" required minlength="6" />
      <input v-model="confirmPassword" type="password" placeholder="Подтвердите пароль" required minlength="6" />

      <div v-if="password && confirmPassword && password !== confirmPassword" class="error-text">
        Пароли не совпадают
      </div>

      <button type="submit" :disabled="loading || !isValid">
        {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
      </button>
      
      <div v-if="error" class="error-text">{{ error }}</div>
      
      <div v-if="success" class="success-text">
        ✅ Регистрация успешна! 
        <br>
        <strong>📬 Нажмите кнопку "Почта" вверху, чтобы подтвердить email.</strong>
      </div>
    </form>
    
    <div class="links">
      Уже есть аккаунт?
      <router-link to="/login">Войти</router-link>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
      error: '',
      success: false
    }
  },
  computed: {
    isValid() {
      return this.password === this.confirmPassword && 
             this.password.length >= 6 &&
             this.username.length >= 3 &&
             this.email.includes('@')
    }
  },
  methods: {
    async register() {
      if (this.password !== this.confirmPassword) {
        this.error = 'Пароли не совпадают'
        return
      }

      this.loading = true
      this.error = ''
      this.success = false
      
      try {
        await api.post('/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        })
        this.success = true
        this.username = ''
        this.email = ''
        this.password = ''
        this.confirmPassword = ''
      } catch (error) {
        this.error = 'Ошибка регистрации: ' + (error.response?.data?.detail || 'неизвестная ошибка')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.error-text {
  color: #e53e3e;
  font-size: 14px;
  text-align: center;
  margin-top: -5px;
}

.success-text {
  color: #27ae60;
  font-size: 14px;
  text-align: center;
  margin-top: -5px;
  line-height: 1.6;
}
</style>