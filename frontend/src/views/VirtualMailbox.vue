<template>
  <div v-if="isOpen" class="mailbox-overlay">
    <div class="mailbox-panel">
      <div class="mailbox-header">
        <div class="header-content">
          <span class="icon"></span>
          <h3>Virtual Mailbox</h3>
        </div>
        <div class="header-actions">
          <button @click="fetchEmails" class="icon-btn" title="Обновить"></button>
          <button @click="$emit('close')" class="icon-btn close-btn">✕</button>
        </div>
      </div>

      <div class="mailbox-body">
        <div v-if="loading && emails.length === 0" class="empty-state">
          <span class="empty-icon"></span>
          <p>Загрузка...</p>
        </div>
        <div v-else-if="emails.length === 0" class="empty-state">
          <span class="empty-icon"></span>
          <p>Пусто</p>
        </div>

        <div v-for="email in emails" :key="email.id" class="email-card">
          <div class="email-header">
            <span class="email-to">{{ email.to }}</span>
            <span class="email-time">{{ new Date(email.sent_at).toLocaleTimeString() }}</span>
          </div>

          <div class="email-content">
            <div class="email-subject">{{ email.subject }}</div>
            <div class="email-body" v-html="email.html" />
          </div>

          <button 
            @click="handleEmailAction(email, email.html)"
            class="email-action-btn"
          >
            <span v-if="isResetEmail(email)">
              Сбросить пароль
            </span>
            <span v-else>
              Подтвердить email
            </span>
          </button>
        </div>
      </div>

      <div v-if="emails.length > 0" class="mailbox-footer">
        <button @click="clearMailbox" :disabled="loading" class="clear-btn">
          Очистить
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  props: {
    isOpen: Boolean
  },
  emits: ['close', 'selectToken', 'selectResetToken'],
  setup(props, { emit }) {
    const emails = ref([])
    const loading = ref(false)
    let intervalId = null

    const isResetEmail = (email) => {
      return email.subject && email.subject.includes('Сброс пароля')
    }

    const fetchEmails = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/diagnostic/emails')
        if (res.ok) {
          const data = await res.json()
          emails.value = data
          console.log('Письма загружены:', data.length)
        }
      } catch (err) {
        console.error('Ошибка загрузки писем:', err)
      }
    }

    const clearMailbox = async () => {
      loading.value = true
      try {
        await fetch('http://localhost:8000/api/diagnostic/emails', { method: 'DELETE' })
        emails.value = []
      } catch (err) {
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const handleEmailAction = (email, htmlContent) => {
      if (email.subject && email.subject.includes('Сброс пароля')) {
        const tokenMatch = htmlContent.match(/\?token=([a-zA-Z0-9_\-]+)/)
        if (tokenMatch) {
          console.log('Сброс пароля, токен:', tokenMatch[1])
          emit('selectResetToken', tokenMatch[1])
          emit('close')
        }
        return
      }


      const tokenMatch = htmlContent.match(/\?token=([a-zA-Z0-9_\-]+)/)
      if (tokenMatch) {
        console.log('Подтверждение email, токен:', tokenMatch[1])
        emit('selectToken', tokenMatch[1])
        emit('close')
      }
    }

    onMounted(() => {
      fetchEmails()
      intervalId = setInterval(fetchEmails, 3000)
    })

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId)
    })

    return {
      emails,
      loading,
      fetchEmails,
      clearMailbox,
      handleEmailAction,
      isResetEmail
    }
  }
}
</script>

<style scoped>
.mailbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
}

.mailbox-panel {
  width: 100%;
  max-width: 420px;
  background: white;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.mailbox-header {
  padding: 16px 20px;
  background: #2d3748;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-content h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: rgba(255,255,255,0.1);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: rgba(255,255,255,0.2);
}

.close-btn:hover {
  background: #e53e3e;
}

.mailbox-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f7fafc;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #a0aec0;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-hint {
  font-size: 12px;
  margin-top: 4px;
}

.email-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 12px;
  transition: box-shadow 0.2s;
}

.email-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.email-header {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 8px;
}

.email-to {
  font-family: monospace;
}

.email-time {
  color: #a0aec0;
}

.email-subject {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
  color: #2d3748;
}

.email-body {
  font-size: 13px;
  color: #4a5568;
  background: #f7fafc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  max-height: 120px;
  overflow-y: auto;
}

.email-body :deep(a) {
  color: #EE82EE;
  word-break: break-all;
}

.email-action-btn {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  color: white;
  background: #27ae60;
}

.email-action-btn:hover {
  background: #219a52;
}

.mailbox-footer {
  padding: 12px 16px;
  border-top: 1px solid #e2e8f0;
  background: white;
  flex-shrink: 0;
}

.clear-btn {
  width: 100%;
  padding: 8px;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.clear-btn:hover {
  background: #c53030;
}

.clear-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>