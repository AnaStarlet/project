<template>
  <div class="container">
    <div v-if="loading" class="loading">
      <h2>Проверка email...</h2>
      <p>Пожалуйста, подождите</p>
    </div>
    <div v-else-if="success" class="success">
      <h2>Email подтвержден!</h2>
      <p>Ваш email успешно подтвержден. Теперь вы можете войти в систему.</p>
      <button @click="goToLogin">Войти</button>
    </div>
    <div v-else class="error">
      <h2>Ошибка подтверждения</h2>
      <p>{{ errorMessage || 'Неверный или просроченный токен' }}</p>
      <button @click="goToLogin">Вернуться к входу</button>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  data() {
    return {
      loading: true,
      success: false,
      errorMessage: '',
    }
  },
  async mounted() {
    const token = new URLSearchParams(window.location.search).get('token')
    if (!token) {
      this.loading = false
      this.errorMessage = 'Токен не найден'
      return
    }

    try {
      await api.get(`/auth/verify-email?token=${token}`)
      this.success = true
      this.loading = false
    } catch (error) {
      this.loading = false
      this.errorMessage = error.response?.data?.detail || 'Ошибка подтверждения'
    }
  },
  methods: {
    goToLogin() {
      window.location.href = '/'
    },
  },
}
</script>

<style scoped>
.loading, .success, .error {
  text-align: center;
  padding: 40px 20px;
}
.loading {
  color: #EE82EE;
}
.success {
  color: #27ae60;
}
.success button {
  margin-top: 20px;
}
.error {
  color: #e74c3c;
}
.error button {
  margin-top: 20px;
  background: #e74c3c;
}
.error button:hover {
  background: #c0392b;
}
</style>