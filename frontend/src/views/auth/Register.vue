<template>
  <div class="register-container">
    <div class="register-card">
      <h2>Crear Cuenta</h2>
      <p class="subtitle">Regístrate en el Sistema de Biblioteca</p>

      <form @submit.prevent="registrarUsuario">
        <div class="form-group">
          <label for="nombre">Nombre Completo:</label>
          <input
            type="text"
            id="nombre"
            v-model="nombre"
            placeholder="Juan López"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Correo Electrónico:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="usuario@ejemplo.com"
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

        <div class="form-group">
          <label for="confirmPassword">Confirmar Contraseña:</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="••••••••"
            required
          />
        </div>

        <div v-if="error" class="alert-error">
          {{ error }}
        </div>
        <div v-if="mensajeExito" class="alert-exito">
          {{ mensajeExito }}
        </div>

        <button type="submit" :disabled="cargando" class="btn-submit">
          {{ cargando ? 'Registrando...' : 'Crear Cuenta' }}
        </button>

        <div class="enlace-login">
          ¿Ya tienes cuenta?
          <router-link to="/login">Inicia Sesión aquí</router-link>
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
  name: 'Register',
  setup() {
    const router = useRouter()
    const nombre = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const error = ref('')
    const mensajeExito = ref('')
    const cargando = ref(false)

    const registrarUsuario = async () => {
      error.value = ''
      mensajeExito.value = ''

      if (password.value !== confirmPassword.value) {
        error.value = 'Las contraseñas no coinciden.'
        return
      }

      cargando.value = true

      try {
        await apiClient.post('/auth/register', {
          nombre: nombre.value,
          email: email.value,
          password: password.value,
          rol: 'admin'
        })

        mensajeExito.value = '¡Cuenta creada con éxito! Redirigiendo al login...'
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al registrar usuario.'
      } finally {
        cargando.value = false
      }
    }

    return {
      nombre,
      email,
      password,
      confirmPassword,
      error,
      mensajeExito,
      cargando,
      registrarUsuario
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 65vh;
}

.register-card {
  background: #ffffff;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 440px;
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
  margin-bottom: 1.1rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 500;
  color: #34495e;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 0.95rem;
}

input:focus {
  outline: none;
  border-color: #27ae60;
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

.alert-exito {
  background-color: #d4efdf;
  color: #1e8449;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-submit {
  width: 100%;
  padding: 0.85rem;
  background-color: #27ae60;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background-color 0.2s ease;
}

.btn-submit:hover:not(:disabled) {
  background-color: #219653;
}

.btn-submit:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.enlace-login {
  margin-top: 1.25rem;
  text-align: center;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.enlace-login a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}
</style>
