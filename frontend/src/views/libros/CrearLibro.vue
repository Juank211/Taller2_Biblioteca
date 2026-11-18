<template>
  <div class="crear-libro-container">
    <div class="card">
      <h2>Registrar Nuevo Libro</h2>
      <p class="subtitle">Ingresa los datos generales del libro (la portada se sube posteriormente)</p>

      <form @submit.prevent="guardarLibro">
        <div class="form-group">
          <label for="titulo">Título:</label>
          <input type="text" id="titulo" v-model="form.titulo" required placeholder="Cien Años de Soledad" />
        </div>

        <div class="form-group">
          <label for="autor">Autor:</label>
          <input type="text" id="autor" v-model="form.autor" required placeholder="Gabriel García Márquez" />
        </div>

        <div class="form-group">
          <label for="isbn">ISBN:</label>
          <input type="text" id="isbn" v-model="form.isbn" required placeholder="978-0307474728" />
        </div>

        <div class="form-group">
          <label for="copias">Copias Disponibles:</label>
          <input type="number" id="copias" v-model.number="form.copias_disponibles" min="1" required />
        </div>

        <div class="form-group">
          <label for="estado">Estado:</label>
          <select id="estado" v-model="form.estado" required>
            <option value="Disponible">Disponible</option>
            <option value="No Disponible">No Disponible</option>
          </select>
        </div>

        <div class="botones">
          <router-link to="/libros" class="btn-cancelar">Cancelar</router-link>
          <button type="submit" class="btn-guardar" :disabled="cargando">
            {{ cargando ? 'Guardando...' : 'Guardar Libro' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiService from '@/services/api'

export default {
  name: 'CrearLibro',
  setup() {
    const router = useRouter()
    const cargando = ref(false)

    const form = ref({
      titulo: '',
      autor: '',
      isbn: '',
      copias_disponibles: 1,
      estado: 'Disponible'
    })

    const guardarLibro = async () => {
      cargando.value = true
      try {
        await apiService.post('/libros/', form.value)
        alert('Libro registrado exitosamente')
        router.push('/libros')
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al registrar libro')
      } finally {
        cargando.value = false
      }
    }

    return {
      form,
      cargando,
      guardarLibro
    }
  }
}
</script>

<style scoped>
.crear-libro-container {
  max-width: 550px;
  margin: 0 auto;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

h2 {
  color: #2c3e50;
  margin-bottom: 0.3rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 500;
  color: #34495e;
}

input, select {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 0.95rem;
}

.botones {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancelar {
  padding: 0.7rem 1.2rem;
  background-color: #e0e0e0;
  color: #333;
  text-decoration: none;
  border-radius: 4px;
}

.btn-guardar {
  padding: 0.7rem 1.4rem;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}
</style>
