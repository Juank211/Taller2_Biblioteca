<template>
  <div id="app-container">
    <header class="navbar">
      <div class="nav-brand">
        <router-link to="/">📚 Biblioteca</router-link>
      </div>

      <nav class="nav-links">
        <template v-if="estaAutenticado">
          <router-link to="/libros">Libros</router-link>
          <router-link to="/usuarios">Usuarios</router-link>
          <router-link to="/prestamos/crear">Préstamos</router-link>
          <router-link to="/usuarios/me">Mi Perfil</router-link>
          <span class="user-badge">{{ userEmail }}</span>
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
      <p>&copy; 2026 Sistema de Gestión de Biblioteca - Taller 2</p>
    </footer>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const estaAutenticado = ref(false)
    const userEmail = ref('')

    const checkAuth = () => {
      const token = localStorage.getItem('access_token')
      estaAutenticado.value = Boolean(token)
      userEmail.value = localStorage.getItem('user_email') || ''
    }

    // Revisar autenticación cada vez que cambie la ruta
    watch(() => route.path, checkAuth, { immediate: true })

    const cerrarSesion = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_email')
      estaAutenticado.value = false
      userEmail.value = ''
      router.push('/login')
    }

    return {
      estaAutenticado,
      userEmail,
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
  background-color: #f5f7fb;
  color: #333333;
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
  background-color: #2c3e50;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-brand a {
  color: #ffffff;
  font-size: 1.4rem;
  font-weight: 700;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.nav-links a {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #3498db;
}

.nav-registro {
  background-color: #27ae60;
  color: white !important;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
}

.nav-registro:hover {
  background-color: #219653;
}

.user-badge {
  color: #bdc3c7;
  font-size: 0.85rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
}

.btn-logout {
  background-color: transparent;
  color: #e74c3c;
  border: 1px solid #e74c3c;
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background-color: #e74c3c;
  color: white;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.footer {
  text-align: center;
  padding: 1rem;
  background-color: #ffffff;
  color: #7f8c8d;
  font-size: 0.9rem;
  border-top: 1px solid #e0e0e0;
}
</style>
