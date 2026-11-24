<template>
  <div class="mis-prestamos-page">
    <div class="header-section">
      <div>
        <h2>🔖 Mis Libros en Préstamo</h2>
        <p class="subtitle">Consulta tus libros prestados, fechas límite (14 días) y estado de entrega.</p>
      </div>
      <router-link to="/libros" class="btn-explorar">📚 Explorar más libros</router-link>
    </div>

    <!-- Indicadores rápidos -->
    <div class="stats-pills">
      <div class="stat-pill">
        <span class="stat-num">{{ activos.length }}</span>
        <span class="stat-txt">Libros en mi poder</span>
      </div>
      <div class="stat-pill stat-alerta" v-if="porVencer.length > 0">
        <span class="stat-num">⚠️ {{ porVencer.length }}</span>
        <span class="stat-txt">Por vencer (&le; 3 días)</span>
      </div>
      <div class="stat-pill stat-danger" v-if="vencidos.length > 0">
        <span class="stat-num">🛑 {{ vencidos.length }}</span>
        <span class="stat-txt">Vencidos (Generando multa)</span>
      </div>
    </div>

    <!-- Selector de vista -->
    <div class="tabs-nav">
      <button
        :class="['tab-btn', tabActiva === 'activos' ? 'active' : '']"
        @click="tabActiva = 'activos'"
      >
        📖 Activos ({{ activos.length }})
      </button>
      <button
        :class="['tab-btn', tabActiva === 'historial' ? 'active' : '']"
        @click="tabActiva = 'historial'"
      >
        📜 Historial Devueltos ({{ devueltos.length }})
      </button>
    </div>

    <div v-if="cargando" class="loading">Cargando tus préstamos...</div>

    <!-- Vista Activos -->
    <div v-else-if="tabActiva === 'activos'">
      <div v-if="activos.length === 0" class="empty-state">
        <p class="empty-icon">🎉</p>
        <p>No tienes libros pendientes de devolución en este momento.</p>
        <router-link to="/libros" class="btn-catalogo">Ir al Catálogo</router-link>
      </div>

      <div v-else class="prestamos-grid">
        <div
          v-for="p in activos"
          :key="p.id"
          :class="['prestamo-card', p.vencido ? 'card-vencido' : (p.dias_restantes <= 3 ? 'card-urgente' : 'card-normal')]"
        >
          <div class="card-cover">
            <img
              v-if="p.libro_portada_url"
              :src="p.libro_portada_url"
              :alt="p.libro_titulo"
              class="cover-img"
            />
            <div v-else class="cover-placeholder">📖</div>

            <!-- Semáforo flotante -->
            <div v-if="p.vencido" class="traffic-badge badge-vencido">
              🛑 Vencido hace {{ p.dias_retraso }} día(s)
            </div>
            <div v-else-if="p.dias_restantes <= 3" class="traffic-badge badge-urgente">
              ⚠️ Vence en {{ p.dias_restantes }} día(s)
            </div>
            <div v-else class="traffic-badge badge-aldia">
              🟢 {{ p.dias_restantes }} días restantes
            </div>
          </div>

          <div class="card-body">
            <h3 class="card-title">{{ p.libro_titulo }}</h3>
            <p class="card-author">✍️ {{ p.libro_autor }}</p>

            <div class="fechas-info">
              <div class="fecha-item">
                <span class="label">Prestado:</span>
                <span class="val">{{ formatearFecha(p.fecha_prestamo) }}</span>
              </div>
              <div class="fecha-item">
                <span class="label">Fecha Límite:</span>
                <span class="val fecha-destacada">{{ formatearFecha(p.fecha_limite) }}</span>
              </div>
            </div>

            <div v-if="p.vencido && p.multa_estimada > 0" class="multa-box">
              ⚠️ Multa acumulada estimada: <strong>${{ p.multa_estimada.toLocaleString() }}</strong>
            </div>

            <button
              @click="devolverLibro(p)"
              :disabled="procesandoDevolucion === p.id"
              class="btn-devolver"
            >
              {{ procesandoDevolucion === p.id ? 'Entregando...' : '📥 Devolver Libro' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista Historial Devueltos -->
    <div v-else>
      <div v-if="devueltos.length === 0" class="empty-state">
        Aún no has registrado devoluciones.
      </div>
      <div v-else class="historial-lista">
        <div v-for="p in devueltos" :key="p.id" class="historial-item">
          <div class="historial-thumb">
            <img v-if="p.libro_portada_url" :src="p.libro_portada_url" :alt="p.libro_titulo" />
            <span v-else>📖</span>
          </div>
          <div class="historial-info">
            <h4>{{ p.libro_titulo }}</h4>
            <p>{{ p.libro_autor }}</p>
          </div>
          <div class="historial-fechas">
            <span>Prestado: {{ formatearFecha(p.fecha_prestamo) }}</span>
            <span class="tag-devuelto">Devuelto: {{ formatearFecha(p.fecha_devuelto) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'MisPrestamos',
  setup() {
    const prestamos = ref([])
    const cargando = ref(true)
    const tabActiva = ref('activos')
    const procesandoDevolucion = ref(null)

    const cargarPrestamos = async () => {
      cargando.value = true
      try {
        prestamos.value = await apiService.get('/prestamos/mis-prestamos')
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al cargar tus préstamos')
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

    const activos = computed(() => prestamos.value.filter(p => !p.fecha_devuelto))
    const devueltos = computed(() => prestamos.value.filter(p => Boolean(p.fecha_devuelto)))
    const porVencer = computed(() => activos.value.filter(p => !p.vencido && p.dias_restantes <= 3))
    const vencidos = computed(() => activos.value.filter(p => p.vencido))

    const devolverLibro = async (prestamo) => {
      if (!confirm(`¿Confirmas la entrega del libro "${prestamo.libro_titulo}"?`)) {
        return
      }

      procesandoDevolucion.value = prestamo.id
      try {
        await apiService.put(`/prestamos/${prestamo.id}/devolver`)
        alert('¡Libro devuelto exitosamente! Gracias por tu puntualidad.')
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
      tabActiva,
      procesandoDevolucion,
      formatearFecha,
      activos,
      devueltos,
      porVencer,
      vencidos,
      devolverLibro
    }
  }
}
</script>

<style scoped>
.mis-prestamos-page {
  max-width: 1100px;
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

.btn-explorar {
  background-color: #3498db;
  color: white;
  padding: 0.65rem 1.25rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.btn-explorar:hover {
  background-color: #2980b9;
}

.stats-pills {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.stat-pill {
  background: white;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stat-num {
  font-weight: 700;
  font-size: 1.2rem;
  color: #2c3e50;
}

.stat-txt {
  font-size: 0.85rem;
  color: #64748b;
}

.stat-alerta {
  border-left: 4px solid #f39c12;
}

.stat-danger {
  border-left: 4px solid #e74c3c;
  background: #fff8f7;
}

.tabs-nav {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.tab-btn {
  background: transparent;
  border: none;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.tab-btn.active {
  background: #3498db;
  color: white;
}

/* Grilla de Préstamos */
.prestamos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.prestamo-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
  transition: transform 0.2s ease;
}

.prestamo-card:hover {
  transform: translateY(-3px);
}

.card-urgente {
  border-top: 4px solid #f39c12;
}

.card-vencido {
  border-top: 4px solid #e74c3c;
  background: #fffcfc;
}

.card-normal {
  border-top: 4px solid #27ae60;
}

.card-cover {
  position: relative;
  height: 200px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  font-size: 2.5rem;
  color: #94a3b8;
}

.traffic-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.badge-aldia {
  background: #27ae60;
  color: white;
}

.badge-urgente {
  background: #f39c12;
  color: white;
}

.badge-vencido {
  background: #e74c3c;
  color: white;
}

.card-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-title {
  font-size: 1.1rem;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.card-author {
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.fechas-info {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.fecha-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.fecha-item .label {
  color: #64748b;
}

.fecha-item .val {
  font-weight: 600;
  color: #334155;
}

.fecha-destacada {
  color: #1e293b;
}

.multa-box {
  background: #fadbd8;
  color: #78281f;
  padding: 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-devolver {
  margin-top: auto;
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-devolver:hover:not(:disabled) {
  background-color: #219653;
}

/* Historial */
.historial-lista {
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.historial-item {
  display: flex;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  gap: 1rem;
}

.historial-item:last-child {
  border-bottom: none;
}

.historial-thumb {
  width: 40px;
  height: 55px;
  background: #f1f5f9;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.historial-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.historial-info {
  flex: 1;
}

.historial-info h4 {
  margin: 0 0 0.2rem 0;
  font-size: 0.95rem;
  color: #1e293b;
}

.historial-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #64748b;
}

.historial-fechas {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #64748b;
}

.tag-devuelto {
  color: #27ae60;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  background: white;
  border-radius: 8px;
  color: #64748b;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.btn-catalogo {
  display: inline-block;
  margin-top: 1rem;
  background: #3498db;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}
</style>
