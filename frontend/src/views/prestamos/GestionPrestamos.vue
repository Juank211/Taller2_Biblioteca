<template>
  <div class="gestion-prestamos">
    <div class="header-section">
      <div>
        <h2>📋 Gestión Integral de Préstamos</h2>
        <p class="subtitle">Monitoreo de préstamos activos, fechas límite (14 días) y control de devoluciones</p>
      </div>
      <router-link to="/prestamos/crear" class="btn-crear">➕ Registrar Préstamo</router-link>
    </div>

    <!-- Filtros y Búsqueda -->
    <div class="filtros-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input
          type="text"
          v-model="busqueda"
          placeholder="Buscar por libro, usuario o correo..."
        />
      </div>

      <div class="filter-pills">
        <button
          :class="['filter-pill', filtroEstado === 'todos' ? 'active' : '']"
          @click="filtroEstado = 'todos'"
        >
          Todos ({{ prestamos.length }})
        </button>
        <button
          :class="['filter-pill', filtroEstado === 'activos' ? 'active' : '']"
          @click="filtroEstado = 'activos'"
        >
          Activos ({{ contadorActivos }})
        </button>
        <button
          :class="['filter-pill pill-vencidos', filtroEstado === 'vencidos' ? 'active' : '']"
          @click="filtroEstado = 'vencidos'"
        >
          🔴 Vencidos ({{ contadorVencidos }})
        </button>
        <button
          :class="['filter-pill', filtroEstado === 'devueltos' ? 'active' : '']"
          @click="filtroEstado = 'devueltos'"
        >
          Devueltos ({{ contadorDevueltos }})
        </button>
      </div>
    </div>

    <!-- Mensaje si está cargando o vacío -->
    <div v-if="cargando" class="loading">Cargando préstamos...</div>
    <div v-else-if="prestamosFiltrados.length === 0" class="empty-state">
      No se encontraron préstamos con los criterios seleccionados.
    </div>

    <!-- Tabla de Préstamos -->
    <div v-else class="table-container">
      <table class="tabla-prestamos">
        <thead>
          <tr>
            <th>Libro</th>
            <th>Usuario Lector</th>
            <th>Fecha Préstamo</th>
            <th>Fecha Límite (14 días)</th>
            <th>Estado & Semáforo</th>
            <th class="text-center">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in prestamosFiltrados" :key="p.id" :class="{'fila-vencida': !p.fecha_devuelto && p.vencido}">
            <!-- Libro -->
            <td class="col-libro">
              <div class="libro-info-group">
                <img
                  v-if="p.libro_portada_url"
                  :src="p.libro_portada_url"
                  :alt="p.libro_titulo"
                  class="thumb-cover"
                />
                <div v-else class="thumb-placeholder">📖</div>
                <div>
                  <strong class="libro-title">{{ p.libro_titulo }}</strong>
                  <span class="libro-sub">{{ p.libro_autor }}</span>
                </div>
              </div>
            </td>

            <!-- Usuario -->
            <td class="col-usuario">
              <div class="usuario-name">👤 {{ p.usuario_nombre }}</div>
              <div class="usuario-email">{{ p.usuario_email }}</div>
            </td>

            <!-- Fecha Préstamo -->
            <td>{{ formatearFecha(p.fecha_prestamo) }}</td>

            <!-- Fecha Límite -->
            <td>
              <strong>{{ formatearFecha(p.fecha_limite) }}</strong>
            </td>

            <!-- Semáforo de Estado -->
            <td>
              <div v-if="p.fecha_devuelto" class="badge-status badge-devuelto">
                ✅ Devuelto ({{ formatearFecha(p.fecha_devuelto) }})
              </div>
              <div v-else-if="p.vencido" class="badge-status badge-vencido">
                🔴 Vencido hace {{ p.dias_retraso }} día(s)
                <span v-if="p.multa_estimada > 0" class="multa-tag">Multa: ${{ p.multa_estimada.toLocaleString() }}</span>
              </div>
              <div v-else-if="p.dias_restantes <= 3" class="badge-status badge-urgente">
                🟡 Vence pronto ({{ p.dias_restantes }} día{{ p.dias_restantes === 1 ? '' : 's' }})
              </div>
              <div v-else class="badge-status badge-aldia">
                🟢 Al día ({{ p.dias_restantes }} días restantes)
              </div>
            </td>

            <!-- Acciones -->
            <td class="text-center">
              <button
                v-if="!p.fecha_devuelto"
                @click="registrarDevolucion(p)"
                :disabled="procesandoDevolucion === p.id"
                class="btn-devolver"
              >
                {{ procesandoDevolucion === p.id ? 'Procesando...' : '📥 Marcar Devolución' }}
              </button>
              <span v-else class="completado-tag">Finalizado</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'GestionPrestamos',
  setup() {
    const prestamos = ref([])
    const cargando = ref(true)
    const busqueda = ref('')
    const filtroEstado = ref('activos')
    const procesandoDevolucion = ref(null)

    const cargarPrestamos = async () => {
      cargando.value = true
      try {
        prestamos.value = await apiService.get('/prestamos/')
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al cargar listado de préstamos')
      } finally {
        cargando.value = false
      }
    }

    const formatearFecha = (fechaStr) => {
      if (!fechaStr) return '-'
      const d = new Date(fechaStr)
      return d.toLocaleDateString('es-CO', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      })
    }

    const contadorActivos = computed(() => {
      return prestamos.value.filter(p => !p.fecha_devuelto).length
    })

    const contadorVencidos = computed(() => {
      return prestamos.value.filter(p => !p.fecha_devuelto && p.vencido).length
    })

    const contadorDevueltos = computed(() => {
      return prestamos.value.filter(p => Boolean(p.fecha_devuelto)).length
    })

    const prestamosFiltrados = computed(() => {
      return prestamos.value.filter(p => {
        // Filtro por estado
        if (filtroEstado.value === 'activos' && p.fecha_devuelto) return false
        if (filtroEstado.value === 'vencidos' && (p.fecha_devuelto || !p.vencido)) return false
        if (filtroEstado.value === 'devueltos' && !p.fecha_devuelto) return false

        // Filtro por búsqueda de texto
        if (busqueda.value.trim()) {
          const q = busqueda.value.toLowerCase()
          const matchLibro = p.libro_titulo.toLowerCase().includes(q)
          const matchAutor = (p.libro_autor || '').toLowerCase().includes(q)
          const matchUsuario = (p.usuario_nombre || '').toLowerCase().includes(q)
          const matchEmail = (p.usuario_email || '').toLowerCase().includes(q)
          return matchLibro || matchAutor || matchUsuario || matchEmail
        }

        return true
      })
    })

    const registrarDevolucion = async (prestamo) => {
      if (!confirm(`¿Confirmas la recepción del libro "${prestamo.libro_titulo}" de ${prestamo.usuario_nombre}?`)) {
        return
      }

      procesandoDevolucion.value = prestamo.id
      try {
        await apiService.put(`/prestamos/${prestamo.id}/devolver`)
        alert('Devolución registrada correctamente. El inventario ha sido actualizado.')
        await cargarPrestamos()
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al procesar la devolución.')
      } finally {
        procesandoDevolucion.value = null
      }
    }

    onMounted(cargarPrestamos)

    return {
      prestamos,
      cargando,
      busqueda,
      filtroEstado,
      procesandoDevolucion,
      formatearFecha,
      contadorActivos,
      contadorVencidos,
      contadorDevueltos,
      prestamosFiltrados,
      registrarDevolucion
    }
  }
}
</script>

<style scoped>
.gestion-prestamos {
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
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
  padding: 0.65rem 1.25rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.btn-crear:hover {
  background-color: #219653;
}

/* Filtros */
.filtros-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  padding: 0.5rem 0.8rem;
  flex: 1;
  max-width: 400px;
}

.search-icon {
  margin-right: 0.5rem;
  color: #94a3b8;
}

.search-box input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 0.9rem;
}

.filter-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-pill {
  background: white;
  border: 1px solid #dcdfe6;
  padding: 0.5rem 0.9rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-pill:hover {
  background: #f1f5f9;
}

.filter-pill.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.pill-vencidos.active {
  background: #e74c3c;
  border-color: #e74c3c;
}

/* Tabla */
.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
  border: 1px solid #eef0f3;
}

.tabla-prestamos {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.tabla-prestamos th {
  background-color: #f8fafc;
  color: #475569;
  text-align: left;
  padding: 1rem 1.25rem;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
}

.tabla-prestamos td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.fila-vencida {
  background-color: #fff9f9;
}

.libro-info-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.thumb-cover {
  width: 42px;
  height: 56px;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.thumb-placeholder {
  width: 42px;
  height: 56px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 1.2rem;
}

.libro-title {
  display: block;
  color: #1e293b;
  font-size: 0.95rem;
}

.libro-sub {
  display: block;
  color: #64748b;
  font-size: 0.8rem;
}

.usuario-name {
  font-weight: 600;
  color: #2c3e50;
}

.usuario-email {
  font-size: 0.8rem;
  color: #7f8c8d;
}

/* Semáforos */
.badge-status {
  display: inline-flex;
  flex-direction: column;
  padding: 0.35rem 0.7rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-aldia {
  background: #d4efdf;
  color: #1e8449;
}

.badge-urgente {
  background: #fef9e7;
  color: #b7950b;
}

.badge-vencido {
  background: #fadbd8;
  color: #b03a2e;
}

.badge-devuelto {
  background: #f1f5f9;
  color: #64748b;
}

.multa-tag {
  font-size: 0.75rem;
  color: #78281f;
  margin-top: 2px;
}

.btn-devolver {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 0.5rem 0.9rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-devolver:hover:not(:disabled) {
  background-color: #1f618d;
}

.completado-tag {
  color: #94a3b8;
  font-size: 0.85rem;
  font-style: italic;
}

.text-center {
  text-align: center;
}

.loading, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
  background: white;
  border-radius: 8px;
}
</style>
