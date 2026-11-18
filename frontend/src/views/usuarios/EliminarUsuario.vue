<template>
  <div class="eliminar-usuario">
    <h2>Eliminar Usuario</h2>
    <form @submit.prevent="eliminarUsuario">
      <div class="form-group">
        <label for="usuarioId">ID del Usuario:</label>
        <input type="number" id="usuarioId" v-model="usuarioId" required />
      </div>
      <button type="submit" :disabled="!validarFormulario">Confirmar Eliminación</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'EliminarUsuario',
  setup() {
    const usuarioId = ref('')
    const error = ref('')

    const validarFormulario = () => {
      return usuarioId.value
    }

    const eliminarUsuario = async () => {
      if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
        try {
          await apiService.delete(`/usuarios/${usuarioId.value}`)
          alert('Usuario eliminado exitosamente')
          usuarioId.value = ''
        } catch (err) {
          error.value = err.response?.data?.detail || 'Error al eliminar usuario'
          alert(error.value)
        }
      }
    }

    return {
      usuarioId, error, validarFormulario, eliminarUsuario
    }
  }
}
</script>

<style scoped>
.eliminar-usuario {
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
  background-color: #f44336;
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