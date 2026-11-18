<template>
  <div class="listado-socios">
    <h2>Listado de Socios</h2>
    <router-link to="/socios/crear" class="btn-crear">Nuevo Socio</router-link>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Email</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="socio in socios" :key="socio.id">
          <td>{{ socio.id }}</td>
          <td>{{ socio.nombre }}</td>
          <td>{{ socio.email }}</td>
          <td>{{ socio.activo ? 'Activo' : 'Inactivo' }}</td>
          <td>
            <router-link :to="`/socios/${socio.id}`" class="btn-ver">Ver</router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'ListadoSocios',
  setup() {
    const socios = ref([])
    const error = ref('')

    const cargarSocios = async () => {
      try {
        socios.value = await apiService.get('/socios')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al cargar socios'
        alert(error.value)
      }
    }

    onMounted(cargarSocios)

    return {
      socios, error
    }
  }
}
</script>

<style scoped>
.listado-socios {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.btn-crear {
  display: inline-block;
  margin-bottom: 20px;
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
th {
  background-color: #f2f2f2;
}
.btn-ver {
  color: #4CAF50;
  text-decoration: none;
}
</style>