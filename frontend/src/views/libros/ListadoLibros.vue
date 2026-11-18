<template>
  <div class="catalogo-libros">
    <div class="header-section">
      <h2>Catálogo de Libros</h2>
      <router-link to="/libros/crear" class="btn-crear">+ Nuevo Libro</router-link>
    </div>

    <div v-if="cargando" class="loading">Cargando libros...</div>
    <div v-else-if="libros.length === 0" class="empty">No hay libros registrados en el catálogo.</div>

    <div v-else class="grid-libros">
      <div v-for="libro in libros" :key="libro.id" class="card-libro">
        <div class="portada-wrapper">
          <img
            v-if="libro.portada_url"
            :src="libro.portada_url"
            :alt="libro.titulo"
            class="portada-img"
          />
          <div v-else class="portada-placeholder">
            <span>📖 Sin Portada</span>
          </div>
        </div>

        <div class="info-libro">
          <h3>{{ libro.titulo }}</h3>
          <p class="autor"><strong>Autor:</strong> {{ libro.autor }}</p>
          <p class="isbn"><strong>ISBN:</strong> {{ libro.isbn }}</p>
          <p class="copias"><strong>Disponibles:</strong> {{ libro.copias_disponibles }}</p>
          <span :class="['badge', libro.estado === 'Disponible' ? 'badge-verde' : 'badge-rojo']">
            {{ libro.estado }}
          </span>

          <div class="acciones">
            <label class="btn-subir-portada">
              📷 Subir Portada
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                @change="e => subirPortada(libro.id, e)"
                hidden
              />
            </label>
            <button @click="eliminarLibro(libro.id)" class="btn-eliminar">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiService, { apiClient } from '@/services/api'

export default {
  name: 'ListadoLibros',
  setup() {
    const libros = ref([])
    const cargando = ref(true)

    const cargarLibros = async () => {
      cargando.value = true
      try {
        libros.value = await apiService.get('/libros/')
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al cargar libros')
      } finally {
        cargando.value = false
      }
    }

    const subirPortada = async (libroId, event) => {
      const archivo = event.target.files[0]
      if (!archivo) return

      const formData = new FormData()
      formData.append('archivo', archivo)

      try {
        await apiClient.post(`/libros/${libroId}/portada`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        alert('Portada subida exitosamente a Cloudinary')
        cargarLibros()
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al subir portada a Cloudinary')
      }
    }

    const eliminarLibro = async (libroId) => {
      if (!confirm('¿Seguro que deseas eliminar este libro?')) return
      try {
        await apiService.delete(`/libros/${libroId}`)
        libros.value = libros.value.filter(l => l.id !== libroId)
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al eliminar libro')
      }
    }

    onMounted(cargarLibros)

    return {
      libros,
      cargando,
      subirPortada,
      eliminarLibro
    }
  }
}
</script>

<style scoped>
.catalogo-libros {
  max-width: 1100px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-crear {
  background-color: #27ae60;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
}

.grid-libros {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.card-libro {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.portada-wrapper {
  height: 220px;
  background: #eaeded;
  display: flex;
  align-items: center;
  justify-content: center;
}

.portada-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.portada-placeholder {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.info-libro {
  padding: 1.2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.info-libro h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.autor, .isbn, .copias {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.3rem;
}

.badge {
  display: inline-block;
  align-self: flex-start;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.badge-verde {
  background-color: #d4efdf;
  color: #1e8449;
}

.badge-rojo {
  background-color: #fadbd8;
  color: #b03a2e;
}

.acciones {
  margin-top: auto;
  padding-top: 1rem;
  display: flex;
  gap: 0.5rem;
}

.btn-subir-portada {
  flex: 1;
  background-color: #3498db;
  color: white;
  text-align: center;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
}

.btn-eliminar {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}
</style>
