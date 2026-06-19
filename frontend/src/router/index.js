import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Notes from '../views/Notes.vue'
import EmailVerification from '../views/EmailVerification.vue'
import PasswordReset from '../views/PasswordReset.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/notes', component: Notes, meta: { requiresAuth: true } },
  { path: '/verify-email', component: EmailVerification },
  { path: '/reset-password', component: PasswordReset }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/notes')
  } else {
    next()
  }
})

export default router