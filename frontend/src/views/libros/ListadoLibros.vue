<template>
  <div class="catalogo-libros">
    <div class="header-section">
      <div>
        <h2>📚 Catálogo General de Libros</h2>
        <p class="subtitle">Explora los títulos disponibles en nuestra biblioteca y solicita tu préstamo a 14 días.</p>
      </div>
      <router-link v-if="isAdmin" to="/libros/crear" class="btn-crear">➕ Nuevo Libro</router-link>
    </div>

    <div v-if="cargando" class="loading">Cargando catálogo de libros...</div>
    <div v-else-if="libros.length === 0" class="empty">No hay libros registrados en el catálogo.</div>

    <div v-else class="grid-libros">
      <div v-for="libro in libros" :key="libro.id" class="card-libro">
        <div class="portada-wrapper">
          <img
            v-if="libro.portada_url"
            :src="libro.portada_url"
            :alt="libro.titulo"
            class="portada-img"
            loading="lazy"
          />
          <div v-else class="portada-placeholder">
            <span>📖 Sin Portada</span>
          </div>
        </div>

        <div class="info-libro">
          <h3>{{ libro.titulo }}</h3>
          <p class="autor"><strong>Autor:</strong> {{ libro.autor }}</p>
          <p class="isbn"><strong>ISBN:</strong> {{ libro.isbn }}</p>
          <p class="copias"><strong>Disponibles:</strong> {{ libro.copias_disponibles }} ejemplares</p>
          <span :class="['badge', libro.copias_disponibles > 0 ? 'badge-verde' : 'badge-rojo']">
            {{ libro.copias_disponibles > 0 ? 'Disponible' : 'Agotado' }}
          </span>

          <div class="acciones">
            <!-- Acción para solicitar préstamo (Todos los usuarios) -->
            <button
              v-if="libro.copias_disponibles > 0"
              @click="solicitarPrestamo(libro)"
              :disabled="procesandoPrestamo === libro.id"
              class="btn-solicitar"
            >
              {{ procesandoPrestamo === libro.id ? 'Solicitando...' : '📖 Solicitar Préstamo' }}
            </button>
            <span v-else class="agotado-tag">Agotado temporalmente</span>

            <!-- Acciones exclusivas del Administrador -->
            <template v-if="isAdmin">
              <label class="btn-subir-portada" title="Subir o cambiar portada en Cloudinary">
                📷 Portada
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  @change="e => subirPortada(libro.id, e)"
                  hidden
                />
              </label>
              <button @click="eliminarLibro(libro.id)" class="btn-eliminar" title="Eliminar libro permanentemente">🗑️</button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiService, { apiClient } from '@/services/api'

export default {
  name: 'ListadoLibros',
  setup() {
    const router = useRouter()
    const libros = ref([])
    const cargando = ref(true)
    const procesandoPrestamo = ref(null)
    const userRole = ref(localStorage.getItem('user_role') || 'usuario')

    const isAdmin = computed(() => userRole.value === 'admin')

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

    const solicitarPrestamo = async (libro) => {
      if (!confirm(`¿Confirmas la solicitud de préstamo del libro "${libro.titulo}" por 14 días?`)) {
        return
      }

      procesandoPrestamo.value = libro.id
      try {
        await apiService.post('/prestamos/', {
          libro_id: libro.id,
          estado: 'Activo'
        })
        alert(`¡Préstamo concedido! Tienes 14 días para devolver "${libro.titulo}".`)
        await cargarLibros()
        router.push(isAdmin.value ? '/prestamos' : '/mis-prestamos')
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al solicitar préstamo')
      } finally {
        procesandoPrestamo.value = null
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
      if (!confirm('¿Seguro que deseas eliminar este libro? Esta acción no se puede deshacer.')) return
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
      isAdmin,
      procesandoPrestamo,
      solicitarPrestamo,
      subirPortada,
      eliminarLibro
    }
  }
}
</script>

<style scoped>
.catalogo-libros {
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-section h2 {
  color: #2c3e50;
  margin-bottom: 0.3rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 0.95rem;
}

.btn-crear {
  background-color: #27ae60;
  color: white;
  padding: 0.65rem 1.3rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.btn-crear:hover {
  background-color: #219653;
}

.grid-libros {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.75rem;
}

.card-libro {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-libro:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
}

.portada-wrapper {
  height: 220px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.portada-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.portada-placeholder {
  color: #94a3b8;
  font-size: 1.1rem;
}

.info-libro {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.info-libro h3 {
  margin-bottom: 0.5rem;
  color: #1e293b;
  font-size: 1.15rem;
  line-height: 1.3;
}

.autor, .isbn, .copias {
  font-size: 0.88rem;
  color: #64748b;
  margin-bottom: 0.3rem;
}

.badge {
  display: inline-block;
  align-self: flex-start;
  padding: 0.25rem 0.65rem;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
  margin-top: 0.4rem;
  margin-bottom: 1rem;
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
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-solicitar {
  flex: 1;
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-solicitar:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn-solicitar:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.agotado-tag {
  flex: 1;
  text-align: center;
  font-size: 0.82rem;
  color: #94a3b8;
  font-style: italic;
}

.btn-subir-portada {
  background-color: #f1f5f9;
  color: #334155;
  border: 1px solid #cbd5e1;
  text-align: center;
  padding: 0.55rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.btn-subir-portada:hover {
  background-color: #e2e8f0;
}

.btn-eliminar {
  background-color: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
  padding: 0.55rem 0.65rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.btn-eliminar:hover {
  background-color: #fca5a5;
}

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}
</style>
