<template>
  <div class="crear-usuario">
    <h2>Crear Usuario</h2>
    <form @submit.prevent="crearUsuario">
      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="nombre" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div class="form-group">
        <label for="rol">Rol:</label>
        <select id="rol" v-model="rol" required>
          <option value="usuario">Usuario</option>
          <option value="admin">Administrador</option>
        </select>
      </div>
      <button type="submit" :disabled="!validarFormulario">Crear Usuario</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'CrearUsuario',
  setup() {
    const nombre = ref('')
    const email = ref('')
    const password = ref('')
    const rol = ref('usuario')
    const error = ref('')

    const validarFormulario = () => {
      return nombre.value && email.value && password.value
    }

    const crearUsuario = async () => {
      try {
        const usuarioData = {
          nombre: nombre.value,
          email: email.value,
          password: password.value,
          rol: rol.value
        }
        await apiService.post('/usuarios', usuarioData)
        alert('Usuario creado exitosamente')
        nombre.value = ''
        email.value = ''
        password.value = ''
        rol.value = 'usuario'
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al crear usuario'
        alert(error.value)
      }
    }

    return {
      nombre, email, password, rol, error, validarFormulario, crearUsuario
    }
  }
}
</script>

<style scoped>
.crear-usuario {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input, select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>