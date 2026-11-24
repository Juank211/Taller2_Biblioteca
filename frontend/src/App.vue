<template>
  <div id="app-container">
    <header class="navbar">
      <div class="nav-brand">
        <router-link to="/dashboard">📚 Biblioteca Inteligente</router-link>
      </div>

      <nav class="nav-links">
        <template v-if="estaAutenticado">
          <router-link to="/dashboard">📊 Dashboard</router-link>
          <router-link to="/libros">📚 Libros</router-link>

          <!-- Rutas condicionales por rol -->
          <router-link v-if="!isAdmin" to="/mis-prestamos">🔖 Mis Préstamos</router-link>
          <router-link v-if="isAdmin" to="/prestamos">📋 Préstamos</router-link>
          <router-link v-if="isAdmin" to="/usuarios">👥 Usuarios</router-link>

          <router-link to="/usuarios/me">👤 Mi Perfil</router-link>

          <div class="user-pill">
            <span class="user-name">{{ userName || userEmail }}</span>
            <span :class="['role-badge', isAdmin ? 'role-badge-admin' : 'role-badge-user']">
              {{ isAdmin ? 'Admin' : 'Lector' }}
            </span>
          </div>

          <button @click="cerrarSesion" class="btn-logout">Cerrar Sesión</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-login">Iniciar Sesión</router-link>
          <router-link to="/registro" class="nav-registro">Registrarse</router-link>
        </template>
      </nav>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2026 Sistema de Gestión de Biblioteca - Taller 2 ADSO</p>
    </footer>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const estaAutenticado = ref(false)
    const userEmail = ref('')
    const userName = ref('')
    const userRole = ref('usuario')

    const isAdmin = computed(() => userRole.value === 'admin')

    const checkAuth = () => {
      const token = localStorage.getItem('access_token')
      estaAutenticado.value = Boolean(token)
      userEmail.value = localStorage.getItem('user_email') || ''
      userName.value = localStorage.getItem('user_name') || ''
      userRole.value = localStorage.getItem('user_role') || 'usuario'
    }

    watch(() => route.path, checkAuth, { immediate: true })

    const cerrarSesion = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_email')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_name')
      estaAutenticado.value = false
      userEmail.value = ''
      userName.value = ''
      userRole.value = 'usuario'
      router.push('/login')
    }

    return {
      estaAutenticado,
      userEmail,
      userName,
      userRole,
      isAdmin,
      cerrarSesion
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
}

#app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e293b;
  padding: 0.9rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand a {
  color: #ffffff;
  font-size: 1.3rem;
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.nav-links a {
  color: #cbd5e1;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s ease;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.08);
}

.nav-login {
  color: #ffffff !important;
}

.nav-registro {
  background-color: #27ae60 !important;
  color: white !important;
  padding: 0.45rem 1rem !important;
  border-radius: 6px;
  font-weight: 600 !important;
}

.nav-registro:hover {
  background-color: #219653 !important;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.user-name {
  color: #f1f5f9;
  font-size: 0.85rem;
  font-weight: 500;
}

.role-badge {
  font-size: 0.7rem;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-weight: 700;
  text-transform: uppercase;
}

.role-badge-admin {
  background: #f39c12;
  color: #1e293b;
}

.role-badge-user {
  background: #3498db;
  color: white;
}

.btn-logout {
  background-color: transparent;
  color: #f87171;
  border: 1px solid #f87171;
  padding: 0.35rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background-color: #ef4444;
  color: white;
  border-color: #ef4444;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1250px;
  width: 100%;
  margin: 0 auto;
}

.footer {
  text-align: center;
  padding: 1.25rem;
  background-color: #ffffff;
  color: #64748b;
  font-size: 0.88rem;
  border-top: 1px solid #e2e8f0;
}
</style>
