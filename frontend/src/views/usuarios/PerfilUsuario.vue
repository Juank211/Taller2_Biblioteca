<template>
  <div class="perfil-usuario">
    <h2>Mi Perfil</h2>
    <div v-if="usuario" class="usuario-info">
      <p><strong>ID:</strong> {{ usuario.id }}</p>
      <p><strong>Nombre:</strong> {{ usuario.nombre }}</p>
      <p><strong>Email:</strong> {{ usuario.email }}</p>
      <p><strong>Rol:</strong> {{ usuario.rol }}</p>
    </div>
    <div v-else>
      <p>Cargando información del perfil...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'PerfilUsuario',
  setup() {
    const usuario = ref(null)
    const error = ref('')

    const cargarPerfil = async () => {
      try {
        usuario.value = await apiService.get('/usuarios/me')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al cargar perfil'
        alert(error.value)
      }
    }

    onMounted(cargarPerfil)

    return {
      usuario, error
    }
  }
}
</script>

<style scoped>
.perfil-usuario {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
.usuario-info {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
p {
  margin: 10px 0;
}
</style>