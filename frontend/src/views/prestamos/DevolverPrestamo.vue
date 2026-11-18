<template>
  <div class="devolver-prestamo">
    <h2>Devolver Préstamo</h2>
    <form @submit.prevent="devolverPrestamo">
      <div class="form-group">
        <label for="prestamoId">ID del Préstamo:</label>
        <input type="number" id="prestamoId" v-model="prestamoId" required />
      </div>
      <button type="submit" :disabled="!validarFormulario">Devolver Préstamo</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'DevolverPrestamo',
  setup() {
    const prestamoId = ref('')
    const error = ref('')

    const validarFormulario = () => {
      return prestamoId.value
    }

    const devolverPrestamo = async () => {
      try {
        await apiService.put(`/prestamos/${prestamoId.value}/devolver`)
        alert('Préstamo devuelto exitosamente')
        prestamoId.value = ''
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al devolver préstamo'
        alert(error.value)
      }
    }

    return {
      prestamoId, error, validarFormulario, devolverPrestamo
    }
  }
}
</script>

<style scoped>
.devolver-prestamo {
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
input {
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