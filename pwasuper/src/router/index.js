import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import Home from '../views/Home.vue'
import Historial from '../views/Historial.vue'
import Profile from '../views/Profile.vue'
import Notificaciones from '../views/Notificaciones.vue'
import Support from '../views/Support.vue'
import Supervisor from '../views/Supervisor.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },
  { path: '/historial', name: 'Historial', component: Historial },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/notificaciones', name: 'Notificaciones', component: Notificaciones },
  { path: '/support', name: 'Support', component: Support },
  { path: '/supervisor', name: 'Supervisor', component: Supervisor }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas con roles
router.beforeEach((to, from, next) => {
  const userData = localStorage.getItem('user')
  const isLoggedIn = !!userData
  
  // Si intenta acceder a login o forgot-password y ya está logueado, redirigir según rol
  if ((to.name === 'Login' || to.name === 'ForgotPassword') && isLoggedIn) {
    try {
      const user = JSON.parse(userData)
      if (user.rol === 'supervisor') {
        next({ name: 'Supervisor' })
      } else {
        next({ name: 'Home' })
      }
    } catch {
      localStorage.clear()
      next({ name: 'Login' })
    }
  }
  // Si intenta acceder a rutas protegidas sin estar logueado
  else if (isLoggedIn === false && to.name !== 'Login' && to.name !== 'ForgotPassword') {
    next({ name: 'Login' })
  }
  // Si está logueado, verificar roles
  else if (isLoggedIn) {
    try {
      const user = JSON.parse(userData)
      
      // Verificar acceso a la vista de supervisor
      if (to.name === 'Supervisor' && user.rol !== 'supervisor') {
        console.log('❌ Acceso denegado: Usuario no es supervisor')
        next({ name: 'Home' })
        return
      }
      
      // Si un supervisor intenta acceder a rutas de técnico, redirigir a supervisor
      if (user.rol === 'supervisor' && 
          ['Home', 'Historial', 'Profile', 'Notificaciones', 'Support'].includes(to.name)) {
        console.log('🔄 Supervisor redirigido a vista de supervisión')
        next({ name: 'Supervisor' })
        return
      }
      
      // Si un técnico intenta acceder a supervisor, redirigir a home
      if (user.rol !== 'supervisor' && to.name === 'Supervisor') {
        console.log('🔄 Técnico redirigido a home')
        next({ name: 'Home' })
        return
      }
      
      next()
    } catch (error) {
      console.error('Error parsing user data:', error)
      localStorage.clear()
      next({ name: 'Login' })
    }
  }
  // En cualquier otro caso, permitir la navegación
  else {
    next()
  }
})

export default router
