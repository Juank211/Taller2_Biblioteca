<template>
  <div class="listado-usuarios">
    <h2>Listado de Usuarios</h2>
    <div v-if="isAdmin">
      <router-link to="/usuarios/crear" class="btn-crear">Nuevo Usuario</router-link>
    </div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Email</th>
          <th>Rol</th>
          <th v-if="isAdmin">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="usuario in usuarios" :key="usuario.id">
          <td>{{ usuario.id }}</td>
          <td>{{ usuario.nombre }}</td>
          <td>{{ usuario.email }}</td>
          <td>{{ usuario.rol }}</td>
          <td v-if="isAdmin">
            <button @click="eliminarUsuario(usuario.id)" class="btn-eliminar">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'ListadoUsuarios',
  setup() {
    const usuarios = ref([])
    const currentUser = ref(null)
    const error = ref('')

    const isAdmin = computed(() => currentUser.value?.rol === 'admin')

    const cargarDatos = async () => {
      try {
        usuarios.value = await apiService.get('/usuarios')
        currentUser.value = await apiService.get('/usuarios/me')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al cargar datos'
        alert(error.value)
      }
    }

    const eliminarUsuario = async (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
        try {
          await apiService.delete(`/usuarios/${id}`)
          cargarDatos()
          alert('Usuario eliminado exitosamente')
        } catch (err) {
          error.value = err.response?.data?.detail || 'Error al eliminar usuario'
          alert(error.value)
        }
      }
    }

    onMounted(cargarDatos)

    return {
      usuarios, isAdmin, eliminarUsuario
    }
  }
}
</script>

<style scoped>
.listado-usuarios {
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
.btn-eliminar {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}
</style>