<template>
  <div class="container">
    <h2>Восстановление пароля</h2>
    
    <div v-if="step === 'request'">
      <p>Введите ваш email, и мы отправим ссылку для сброса пароля</p>
      <form @submit.prevent="requestReset">
        <input v-model="email" type="email" placeholder="Email" required />
        <button type="submit">Отправить</button>
      </form>
      <div class="links">
        <a href="#" @click.prevent="goToLogin">Вернуться к входу</a>
      </div>
    </div>

    <div v-else-if="step === 'success'">
      <h2>Письмо отправлено!</h2>
      <p>Проверьте ваш email для сброса пароля</p>
      <button @click="goToLogin">Вернуться к входу</button>
    </div>

    <div v-else-if="step === 'reset'">
      <h2>Сброс пароля</h2>
      <form @submit.prevent="resetPassword">
        <input v-model="newPassword" type="password" placeholder="Новый пароль" required />
        <input v-model="confirmPassword" type="password" placeholder="Подтвердите пароль" required />
        <button type="submit">Сбросить пароль</button>
      </form>
    </div>

    <div v-else-if="step === 'reset-success'">
      <h2>Пароль изменен!</h2>
      <p>Теперь вы можете войти с новым паролем</p>
      <button @click="goToLogin">Войти</button>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  data() {
    return {
      step: 'request',
      email: '',
      newPassword: '',
      confirmPassword: '',
      resetToken: '',
    }
  },
  mounted() {
    const token = new URLSearchParams(window.location.search).get('token')
    if (token) {
      this.step = 'reset'
      this.resetToken = token
    }
  },
  methods: {
    async requestReset() {
      try {
        await api.post('/auth/request-password-reset', null, {
          params: { email: this.email }
        })
        this.step = 'success'
      } catch (error) {
        alert('Ошибка: ' + (error.response?.data?.detail || 'Пользователь не найден'))
      }
    },
    async resetPassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert('Пароли не совпадают')
        return
      }
      if (this.newPassword.length < 6) {
        alert('Пароль должен быть не менее 6 символов')
        return
      }
      try {
        await api.post('/auth/reset-password', {
          token: this.resetToken,
          new_password: this.newPassword,
        })
        this.step = 'reset-success'
      } catch (error) {
        alert('Ошибка: ' + (error.response?.data?.detail || 'Не удалось сбросить пароль'))
      }
    },
    goToLogin() {
      this.$parent.page = 'login'
    },
  },
}
</script>

<style scoped>
p {
  text-align: center;
  margin-bottom: 20px;
  color: #4a5568;
}
.links {
  text-align: center;
  margin-top: 16px;
}
.links a {
  color: #EE82EE;
  text-decoration: none;
  font-weight: 600;
}
.links a:hover {
  text-decoration: underline;
}
</style>