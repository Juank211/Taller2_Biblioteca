<template>
  <div class="crear-socio">
    <h2>Crear Socio</h2>
    <form @submit.prevent="crearSocio">
      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="nombre" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="activo">Estado:</label>
        <select id="activo" v-model="activo">
          <option value="true">Activo</option>
          <option value="false">Inactivo</option>
        </select>
      </div>
      <button type="submit" :disabled="!validarFormulario">Crear Socio</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'CrearSocio',
  setup() {
    const nombre = ref('')
    const email = ref('')
    const activo = ref('true')
    const error = ref('')

    const validarFormulario = () => {
      return nombre.value && email.value
    }

    const crearSocio = async () => {
      try {
        const socioData = {
          nombre: nombre.value,
          email: email.value,
          activo: activo.value === 'true'
        }
        await apiService.post('/socios', socioData)
        alert('Socio creado exitosamente')
        nombre.value = ''
        email.value = ''
        activo.value = 'true'
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al crear socio'
        alert(error.value)
      }
    }

    return {
      nombre, email, activo, error, validarFormulario, crearSocio
    }
  }
}
</script>

<style scoped>
.crear-socio {
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