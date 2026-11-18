<template>
  <div class="prestamo-form">
    <h2>Crear Préstamo</h2>
    <form @submit.prevent="crearPrestamo">
      <div class="form-group">
        <label for="libroId">Libro:</label>
        <select id="libroId" v-model="libroId" required>
          <option value="" disabled>Selecciona un libro</option>
          <option v-for="libro in libros" :key="libro.id" :value="libro.id">
            {{ libro.titulo }} (Copias disponibles: {{ libro.copias_disponibles }})
          </option>
        </select>
      </div>

      <div class="form-group" v-if="usuarios.length > 0">
        <label for="usuarioId">Usuario solicitante:</label>
        <select id="usuarioId" v-model="usuarioId" required>
          <option value="" disabled>Selecciona un usuario</option>
          <option v-for="u in usuarios" :key="u.id" :value="u.id">
            {{ u.nombre }} ({{ u.email }})
          </option>
        </select>
      </div>

      <button type="submit" :disabled="!validarFormulario || cargando">
        {{ cargando ? 'Creando préstamo...' : 'Crear Préstamo' }}
      </button>
    </form>

    <div class="enlace-devolucion">
      <router-link to="/prestamos/devolver/1">¿Deseas registrar una devolución?</router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'CrearPrestamo',
  setup() {
    const libroId = ref('')
    const usuarioId = ref('')
    const libros = ref([])
    const usuarios = ref([])
    const error = ref('')
    const cargando = ref(false)

    const validarFormulario = computed(() => {
      return Boolean(libroId.value)
    })

    const crearPrestamo = async () => {
      cargando.value = true
      try {
        const prestamoData = {
          libro_id: Number(libroId.value),
          usuario_id: Number(usuarioId.value || 1),
          estado: 'Activo'
        }
        await apiService.post('/prestamos/', prestamoData)
        alert('Préstamo creado exitosamente')
        libroId.value = ''
        cargarDatos()
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al crear préstamo'
        alert(error.value)
      } finally {
        cargando.value = false
      }
    }

    const cargarDatos = async () => {
      try {
        const librosData = await apiService.get('/libros/')
        libros.value = librosData.filter(l => l.copias_disponibles > 0)
      } catch (err) {
        console.warn('No se pudieron cargar los libros:', err)
      }

      try {
        usuarios.value = await apiService.get('/usuarios/')
        if (usuarios.value.length > 0 && !usuarioId.value) {
          usuarioId.value = usuarios.value[0].id
        }
      } catch (err) {
        console.warn('No se pudieron cargar usuarios (requiere admin):', err)
      }
    }

    onMounted(cargarDatos)

    return {
      libroId,
      usuarioId,
      libros,
      usuarios,
      error,
      cargando,
      validarFormulario,
      crearPrestamo
    }
  }
}
</script>

<style scoped>
.prestamo-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
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
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 0.95rem;
}
button {
  width: 100%;
  background-color: #27ae60;
  color: white;
  padding: 0.85rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1rem;
}
button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
.enlace-devolucion {
  margin-top: 1.5rem;
  text-align: center;
}
.enlace-devolucion a {
  color: #3498db;
  text-decoration: none;
  font-size: 0.9rem;
}
</style>
