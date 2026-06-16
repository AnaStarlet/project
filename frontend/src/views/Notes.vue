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
      <h3>{{ note.title }}</h3>
      <p>{{ note.content }}</p>
      <div class="actions">
        <button class="danger" @click="deleteNote(note.id)">Удалить</button>
      </div>
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