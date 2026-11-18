<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Iniciar Sesión</h2>
      <p class="subtitle">Accede al Sistema de Biblioteca</p>

      <form @submit.prevent="iniciarSesion">
        <div class="form-group">
          <label for="email">Correo Electrónico:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="admin@test.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="••••••••"
            required
          />
        </div>

        <div v-if="error" class="alert-error">
          {{ error }}
        </div>

        <button type="submit" :disabled="cargando" class="btn-submit">
          {{ cargando ? 'Iniciando sesión...' : 'Entrar' }}
        </button>

        <div class="enlace-registro">
          ¿No tienes una cuenta?
          <router-link to="/registro">Regístrate aquí</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient } from '@/services/api'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const cargando = ref(false)

    const iniciarSesion = async () => {
      error.value = ''
      cargando.value = true

      try {
        // OAuth2PasswordRequestForm espera form-urlencoded
        const params = new URLSearchParams()
        params.append('username', email.value)
        params.append('password', password.value)

        const response = await apiClient.post('/auth/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        const { access_token, refresh_token } = response.data
        localStorage.setItem('access_token', access_token)
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token)
        }
        localStorage.setItem('user_email', email.value)

        router.push('/usuarios')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al autenticar. Verifica tus credenciales.'
      } finally {
        cargando.value = false
      }
    }

    return {
      email,
      password,
      error,
      cargando,
      iniciarSesion
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  background: #ffffff;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #7f8c8d;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #34495e;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #3498db;
}

.alert-error {
  background-color: #fde2e2;
  color: #e74c3c;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-submit {
  width: 100%;
  padding: 0.85rem;
  background-color: #3498db;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-submit:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn-submit:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.enlace-registro {
  margin-top: 1.25rem;
  text-align: center;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.enlace-registro a {
  color: #27ae60;
  text-decoration: none;
  font-weight: 600;
}
</style>
