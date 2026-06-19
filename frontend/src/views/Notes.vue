<template>
  <div class="container">
    <div class="header">
      <h2>Мои заметки</h2>
      <button @click="logout" class="logout-btn">Выйти</button>
    </div>

    <div class="note-form">
      <input v-model="newTitle" placeholder="Заголовок" />
      <textarea v-model="newContent" placeholder="Текст заметки"></textarea>
      <button @click="createNote" :disabled="!newTitle || !newContent">
        Создать
      </button>
    </div>

    <div v-if="notes.length === 0" class="empty">
      У вас пока нет заметок
    </div>

    <div v-for="note in notes" :key="note.id" class="note-card">
      <template v-if="editingNoteId === note.id">
        <input v-model="editTitle" placeholder="Заголовок" />
        <textarea v-model="editContent" placeholder="Текст заметки"></textarea>
        <div class="actions">
          <button @click="saveEdit(note.id)" :disabled="!editTitle || !editContent">Сохранить</button>
          <button class="secondary" @click="cancelEdit">Отмена</button>
        </div>
      </template>

      <template v-else>
        <h3>{{ note.title }}</h3>
        <p>{{ note.content }}</p>
        <div class="actions">
          <button class="secondary" @click="startEdit(note)">Редактировать</button>
          <button class="danger" @click="deleteNote(note.id)">Удалить</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      notes: [],
      newTitle: '',
      newContent: '',
      editingNoteId: null,
      editTitle: '',
      editContent: '',
    }
  },
  async mounted() {
    await this.fetchNotes()
  },
  methods: {
    async fetchNotes() {
      try {
        const response = await api.get('/notes')
        this.notes = response.data
      } catch (error) {
        console.error('Ошибка загрузки заметок:', error)
      }
    },

    async createNote() {
      if (!this.newTitle || !this.newContent) return
      try {
        await api.post('/notes', {
          title: this.newTitle,
          content: this.newContent,
        })
        this.newTitle = ''
        this.newContent = ''
        await this.fetchNotes()
      } catch (error) {
        console.error('Ошибка создания заметки:', error)
      }
    },

    startEdit(note) {
      this.editingNoteId = note.id
      this.editTitle = note.title
      this.editContent = note.content
    },

    cancelEdit() {
      this.editingNoteId = null
      this.editTitle = ''
      this.editContent = ''
    },

    async saveEdit(id) {
      if (!this.editTitle || !this.editContent) return
      try {
        await api.put(`/notes/${id}`, {
          title: this.editTitle,
          content: this.editContent,
        })
        this.cancelEdit()
        await this.fetchNotes()
      } catch (error) {
        console.error('Ошибка обновления заметки:', error)
      }
    },

    async deleteNote(id) {
      if (confirm('Удалить заметку?')) {
        try {
          await api.delete(`/notes/${id}`)
          await this.fetchNotes()
        } catch (error) {
          console.error('Ошибка удаления заметки:', error)
        }
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      this.router.push('/login')
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logout-btn {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

.logout-btn:hover {
  background: #c53030;
}

.note-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f7fafc;
  border-radius: 8px;
}

.note-card {
  padding: 16px;
  margin-bottom: 12px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.note-card h3 {
  margin-bottom: 8px;
  color: #2d3748;
}

.note-card p {
  color: #4a5568;
  white-space: pre-wrap;
  margin-bottom: 12px;
}

.actions {
  display: flex;
  gap: 8px;
}

.empty {
  text-align: center;
  padding: 40px;
  color: #a0aec0;
  font-size: 16px;
}

button.secondary {
  background: #e2e8f0;
  color: #2d3748;
}

button.secondary:hover {
  background: #cbd5e0;
}

button.danger {
  background: #fc8181;
}

button.danger:hover {
  background: #f56565;
}
</style>