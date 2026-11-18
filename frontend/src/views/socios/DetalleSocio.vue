<template>
  <div class="detalle-socio">
    <h2>Detalle del Socio</h2>
    <div v-if="socio" class="socio-info">
      <p><strong>ID:</strong> {{ socio.id }}</p>
      <p><strong>Nombre:</strong> {{ socio.nombre }}</p>
      <p><strong>Email:</strong> {{ socio.email }}</p>
      <p><strong>Estado:</strong> {{ socio.activo ? 'Activo' : 'Inactivo' }}</p>
    </div>
    <div v-else>
      <p>Cargando información del socio...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiService from '@/services/api'

export default {
  name: 'DetalleSocio',
  setup() {
    const route = useRoute()
    const socio = ref(null)
    const error = ref('')

    const cargarSocio = async () => {
      try {
        socio.value = await apiService.get(`/socios/${route.params.id}`)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al cargar el socio'
        alert(error.value)
      }
    }

    onMounted(cargarSocio)

    return {
      socio, error
    }
  }
}
</script>

<style scoped>
.detalle-socio {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
.socio-info {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
p {
  margin: 10px 0;
}
</style>