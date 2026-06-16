<template>
  <div class="container">
    <h2>Мои заметки</h2>

    <div class="note-form">
      <input v-model="newTitle" placeholder="Заголовок" />
      <textarea v-model="newContent" placeholder="Текст заметки"></textarea>
      <button @click="createNote">➕ Создать</button>
    </div>

    <div v-if="notes.length === 0" class="empty">
      У вас пока нет заметок
    </div>

    <div v-for="note in notes" :key="note.id" class="note">
      <!-- Режим редактирования -->
      <template v-if="editingNoteId === note.id">
        <input v-model="editTitle" placeholder="Заголовок" />
        <textarea v-model="editContent" placeholder="Текст заметки"></textarea>
        <div class="actions">
          <button @click="saveEdit(note.id)">Сохранить</button>
          <button class="secondary" @click="cancelEdit">Отмена</button>
        </div>
      </template>

      <!-- Режим просмотра -->
      <template v-else>
        <h3>{{ note.title }}</h3>
        <p>{{ note.content }}</p>
        <div class="actions">
          <button @click="startEdit(note)">Редактировать</button> |
          <button class="danger" @click="deleteNote(note.id)">Удалить</button>
        </div>
      </template>
    </div>

    <button class="logout-btn secondary" @click="logout">Выйти</button>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
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
      const response = await api.get('/notes')
      this.notes = response.data
    },

    async createNote() {
      if (!this.newTitle || !this.newContent) return
      await api.post('/notes', {
        title: this.newTitle,
        content: this.newContent,
      })
      this.newTitle = ''
      this.newContent = ''
      await this.fetchNotes()
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
      await api.put(`/notes/${id}`, {
        title: this.editTitle,
        content: this.editContent,
      })
      this.cancelEdit()
      await this.fetchNotes()
    },

    async deleteNote(id) {
      if (confirm('Удалить заметку?')) {
        await api.delete(`/notes/${id}`)
        await this.fetchNotes()
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      this.$parent.page = 'login'
    },
  },
}
</script>