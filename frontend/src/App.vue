<template>
  <div id="app">
    <div class="nav-bar">
      <div class="nav-links">
        <span class="app-title">Notes App</span>
        <router-link v-if="isAuthenticated" to="/notes">Заметки</router-link>
        <button @click="toggleMailbox" class="mailbox-btn">
          Почта
          <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
        </button>
        <button v-if="isAuthenticated" @click="logout" class="logout-btn">Выйти</button>
        <router-link v-if="!isAuthenticated" to="/login" class="login-link">Войти</router-link>
      </div>
    </div>

    <router-view />
    
    <VirtualMailbox 
      :isOpen="mailboxOpen" 
      @close="mailboxOpen = false"
      @selectToken="handleToken"
      @selectResetToken="handleResetToken"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import VirtualMailbox from './views/VirtualMailbox.vue'

export default {
  components: { VirtualMailbox },
  setup() {
    const router = useRouter()
    const mailboxOpen = ref(false)
    const unreadCount = ref(0)
    let intervalId = null

    const isAuthenticated = computed(() => {
      return !!localStorage.getItem('access_token')
    })

    const toggleMailbox = () => {
      mailboxOpen.value = !mailboxOpen.value
      if (mailboxOpen.value) {
        unreadCount.value = 0
      }
    }

    const logout = () => {
      localStorage.removeItem('access_token')
      router.push('/login')
    }

    const handleToken = (token) => {
      router.push(`/verify-email?token=${token}`)
    }

    const handleResetToken = (token) => {
      router.push(`/reset-password?token=${token}`)
    }

    const checkNewEmails = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/diagnostic/emails')
        if (res.ok) {
          const emails = await res.json()
          const newEmails = emails.filter(e => {
            const sent = new Date(e.sent_at)
            const now = new Date()
            return (now - sent) < 30000
          })
          if (newEmails.length > 0 && !mailboxOpen.value) {
            unreadCount.value = newEmails.length
          }
        }
      } catch (err) {
        // ignore
      }
    }

    onMounted(() => {
      checkNewEmails()
      intervalId = setInterval(checkNewEmails, 5000)
    })

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId)
    })

    return {
      isAuthenticated,
      mailboxOpen,
      unreadCount,
      toggleMailbox,
      logout,
      handleToken,
      handleResetToken
    }
  }
}
</script>

<style>
@import './style.css';

.nav-bar {
  background: #2d3748;
  padding: 12px 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.app-title {
  color: #EE82EE;
  font-weight: bold;
  font-size: 18px;
  margin-right: 20px;
}

.nav-links a {
  color: #e2e8f0;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 4px;
  transition: background 0.2s;
}

.nav-links a:hover {
  background: #4a5568;
}

.nav-links a.router-link-active {
  background: #4a5568;
  color: #EE82EE;
}

.login-link {
  color: #e2e8f0;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 4px;
  transition: background 0.2s;
  margin-left: auto;
}

.login-link:hover {
  background: #4a5568;
}

.mailbox-btn {
  background: #4a5568;
  color: #e2e8f0;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
  font-size: 14px;
}

.mailbox-btn:hover {
  background: #5a6a7e;
}

.badge {
  background: #e53e3e;
  color: white;
  border-radius: 50%;
  padding: 1px 7px;
  font-size: 11px;
  margin-left: 5px;
}

.logout-btn {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: auto;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #c53030;
}
</style>