<template>
  <div class="dashboard-page">
    <!-- Hero Banner -->
    <section class="hero-banner">
      <div class="hero-content">
        <div class="hero-title-group">
          <h1>¡Hola, {{ stats.usuario_nombre || 'Lector' }}! 👋</h1>
          <span :class="['role-pill', stats.es_admin ? 'role-admin' : 'role-user']">
            {{ stats.es_admin ? '🛡️ Administrador' : '📖 Lector de Biblioteca' }}
          </span>
        </div>
        <p class="hero-subtitle">
          Bienvenido a tu panel de control de la biblioteca. Consulta la disponibilidad de libros, fechas límite y estado de tus préstamos.
        </p>
      </div>
      <div class="hero-actions">
        <router-link to="/libros" class="btn-primary">📚 Ver Catálogo</router-link>
        <router-link v-if="stats.es_admin" to="/prestamos" class="btn-secondary">📋 Gestión de Préstamos</router-link>
        <router-link v-else to="/mis-prestamos" class="btn-secondary">🔖 Mis Préstamos ({{ stats.mis_prestamos_activos }})</router-link>
      </div>
    </section>

    <!-- Alertas Dinámicas -->
    <section v-if="stats.alertas && stats.alertas.length > 0" class="alerts-section">
      <div
        v-for="(alerta, index) in stats.alertas"
        :key="index"
        :class="['alert-banner', `alert-${alerta.tipo}`]"
      >
        <div class="alert-icon">
          <span v-if="alerta.tipo === 'danger'">🚨</span>
          <span v-else-if="alerta.tipo === 'warning'">⚠️</span>
          <span v-else>ℹ️</span>
        </div>
        <div class="alert-text">
          <strong>{{ alerta.titulo }}:</strong> {{ alerta.mensaje }}
        </div>
        <router-link v-if="alerta.enlace" :to="alerta.enlace" class="alert-link">
          Ver detalles →
        </router-link>
      </div>
    </section>

    <!-- KPI Metric Cards Grid -->
    <section class="kpi-grid">
      <div class="kpi-card card-libros">
        <div class="kpi-icon">📚</div>
        <div class="kpi-data">
          <span class="kpi-value">{{ stats.total_libros }}</span>
          <span class="kpi-label">Títulos Registrados</span>
        </div>
      </div>

      <div class="kpi-card card-disponibles">
        <div class="kpi-icon">✅</div>
        <div class="kpi-data">
          <span class="kpi-value">{{ stats.total_ejemplares_disponibles }}</span>
          <span class="kpi-label">Copias Disponibles</span>
        </div>
      </div>

      <div class="kpi-card card-prestamos">
        <div class="kpi-icon">🔄</div>
        <div class="kpi-data">
          <span class="kpi-value">
            {{ stats.es_admin ? stats.total_prestamos_activos : stats.mis_prestamos_activos }}
          </span>
          <span class="kpi-label">
            {{ stats.es_admin ? 'Préstamos Totales Activos' : 'Mis Libros en Préstamo' }}
          </span>
        </div>
      </div>

      <div :class="['kpi-card', (stats.es_admin ? stats.prestamos_vencidos_total : stats.mis_prestamos_vencidos) > 0 ? 'card-vencidos-alerta' : 'card-vencidos']">
        <div class="kpi-icon">⏰</div>
        <div class="kpi-data">
          <span class="kpi-value">
            {{ stats.es_admin ? stats.prestamos_vencidos_total : stats.mis_prestamos_vencidos }}
          </span>
          <span class="kpi-label">
            {{ stats.es_admin ? 'Préstamos Vencidos (General)' : 'Mis Préstamos Vencidos' }}
          </span>
        </div>
      </div>
    </section>

    <!-- Sección de Libros Recientes con Portadas Cloudinary -->
    <section class="featured-section">
      <div class="section-header">
        <div>
          <h2>🌟 Catálogo Reciente</h2>
          <p class="section-desc">Últimos libros incorporados con disponibilidad en tiempo real</p>
        </div>
        <router-link to="/libros" class="view-all-link">Explorar todos ({{ stats.total_libros }}) →</router-link>
      </div>

      <div v-if="cargando" class="loading-state">Cargando catálogo...</div>

      <div v-else-if="!stats.libros_recientes || stats.libros_recientes.length === 0" class="empty-state">
        No hay libros disponibles en este momento.
      </div>

      <div v-else class="books-grid">
        <div v-for="libro in stats.libros_recientes" :key="libro.id" class="book-card">
          <div class="book-cover">
            <img
              v-if="libro.portada_url"
              :src="libro.portada_url"
              :alt="libro.titulo"
              class="cover-image"
              loading="lazy"
            />
            <div v-else class="cover-placeholder">
              <span class="book-emoji">📖</span>
              <span class="no-cover-text">Sin portada</span>
            </div>
            <span :class="['badge-floating', libro.copias_disponibles > 0 ? 'badge-disponible' : 'badge-agotado']">
              {{ libro.copias_disponibles > 0 ? `${libro.copias_disponibles} disp.` : 'Agotado' }}
            </span>
          </div>

          <div class="book-details">
            <h3 class="book-title" :title="libro.titulo">{{ libro.titulo }}</h3>
            <p class="book-author">✍️ {{ libro.autor }}</p>
            <p class="book-isbn">ISBN: {{ libro.isbn }}</p>

            <button
              v-if="libro.copias_disponibles > 0"
              @click="solicitarPrestamo(libro)"
              :disabled="procesandoPrestamo === libro.id"
              class="btn-solicitar"
            >
              {{ procesandoPrestamo === libro.id ? 'Solicitando...' : '📖 Pedir Prestado' }}
            </button>
            <button v-else disabled class="btn-agotado">
              No disponible
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiService from '@/services/api'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const cargando = ref(true)
    const procesandoPrestamo = ref(null)
    const stats = ref({
      total_libros: 0,
      total_ejemplares_disponibles: 0,
      total_prestamos_activos: 0,
      total_usuarios: 0,
      es_admin: false,
      usuario_nombre: '',
      usuario_rol: 'usuario',
      prestamos_vencidos_total: 0,
      mis_prestamos_activos: 0,
      mis_prestamos_proximos_vencer: 0,
      mis_prestamos_vencidos: 0,
      alertas: [],
      libros_recientes: []
    })

    const cargarDashboard = async () => {
      cargando.value = true
      try {
        const data = await apiService.get('/dashboard/stats')
        stats.value = data
        if (data.usuario_rol) {
          localStorage.setItem('user_role', data.usuario_rol)
        }
        if (data.usuario_nombre) {
          localStorage.setItem('user_nombre', data.usuario_nombre)
        }
      } catch (err) {
        console.error('Error al cargar dashboard:', err)
      } finally {
        cargando.value = false
      }
    }

    const solicitarPrestamo = async (libro) => {
      if (!confirm(`¿Deseas solicitar el libro "${libro.titulo}" en préstamo por 14 días?`)) {
        return
      }

      procesandoPrestamo.value = libro.id
      try {
        await apiService.post('/prestamos/', {
          libro_id: libro.id,
          estado: 'Activo'
        })
        alert(`¡Préstamo otorgado con éxito! Tienes 14 días para devolver "${libro.titulo}".`)
        await cargarDashboard()
        router.push(stats.value.es_admin ? '/prestamos' : '/mis-prestamos')
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al solicitar el préstamo.')
      } finally {
        procesandoPrestamo.value = null
      }
    }

    onMounted(cargarDashboard)

    return {
      stats,
      cargando,
      procesandoPrestamo,
      solicitarPrestamo
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Hero Banner */
.hero-banner {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  padding: 2.2rem 2.5rem;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 8px 24px rgba(30, 60, 114, 0.2);
  flex-wrap: wrap;
  gap: 1.5rem;
}

.hero-title-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.hero-title-group h1 {
  font-size: 1.9rem;
  font-weight: 700;
  margin: 0;
}

.role-pill {
  font-size: 0.8rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.role-admin {
  background: #f39c12;
  color: #2c3e50;
}

.role-user {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
}

.hero-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  max-width: 650px;
  line-height: 1.5;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary {
  background-color: #27ae60;
  color: white;
  padding: 0.75rem 1.4rem;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 4px 10px rgba(39, 174, 96, 0.3);
}

.btn-primary:hover {
  background-color: #219653;
  transform: translateY(-2px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  padding: 0.75rem 1.4rem;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

/* Alertas */
.alerts-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.alert-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  font-size: 0.95rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.alert-warning {
  background-color: #fef9e7;
  border-left: 5px solid #f39c12;
  color: #7d6608;
}

.alert-danger {
  background-color: #fadbd8;
  border-left: 5px solid #e74c3c;
  color: #78281f;
}

.alert-icon {
  font-size: 1.4rem;
}

.alert-text {
  flex: 1;
}

.alert-link {
  color: inherit;
  font-weight: 700;
  text-decoration: underline;
  white-space: nowrap;
}

/* KPIs */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
}

.kpi-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  border: 1px solid #eef0f3;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
}

.kpi-icon {
  font-size: 2.2rem;
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 12px;
}

.kpi-data {
  display: flex;
  flex-direction: column;
}

.kpi-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.1;
}

.kpi-label {
  font-size: 0.85rem;
  color: #7f8c8d;
  font-weight: 500;
  margin-top: 0.25rem;
}

.card-vencidos-alerta {
  border-left: 4px solid #e74c3c;
  background: #fff8f7;
}

.card-vencidos-alerta .kpi-value {
  color: #c0392b;
}

/* Libros Destacados */
.featured-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  border: 1px solid #eef0f3;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #edf2f7;
}

.section-header h2 {
  font-size: 1.4rem;
  color: #2c3e50;
  margin-bottom: 0.2rem;
}

.section-desc {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.view-all-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.view-all-link:hover {
  text-decoration: underline;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 1.5rem;
}

.book-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background: white;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.book-cover {
  position: relative;
  height: 200px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
}

.book-emoji {
  font-size: 2.2rem;
}

.no-cover-text {
  font-size: 0.8rem;
}

.badge-floating {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.badge-disponible {
  background: #27ae60;
  color: white;
}

.badge-agotado {
  background: #e74c3c;
  color: white;
}

.book-details {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  font-size: 1.05rem;
  color: #1e293b;
  margin-bottom: 0.4rem;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-author {
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.book-isbn {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.btn-solicitar {
  margin-top: auto;
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

.btn-solicitar:hover {
  background-color: #2980b9;
}

.btn-agotado {
  margin-top: auto;
  background-color: #f1f5f9;
  color: #94a3b8;
  border: 1px solid #e2e8f0;
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: not-allowed;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #7f8c8d;
}
</style>
