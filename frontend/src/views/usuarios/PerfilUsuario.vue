<template>
  <div class="perfil-usuario">
    <div class="perfil-card">
      <div class="perfil-header">
        <div class="avatar-circle">
          {{ usuario?.nombre ? usuario.nombre.charAt(0).toUpperCase() : '👤' }}
        </div>
        <h2>Mi Perfil</h2>
        <span :class="['role-tag', usuario?.rol === 'admin' ? 'tag-admin' : 'tag-user']">
          {{ usuario?.rol === 'admin' ? '🛡️ Administrador' : '📖 Lector de Biblioteca' }}
        </span>
      </div>

      <div v-if="cargando" class="loading">
        Cargando información del perfil...
      </div>

      <div v-else-if="usuario" class="usuario-info">
        <div class="info-row">
          <span class="info-label">Identificador:</span>
          <span class="info-value">#{{ usuario.id }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Nombre Completo:</span>
          <span class="info-value">{{ usuario.nombre }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Correo Electrónico:</span>
          <span class="info-value">{{ usuario.email }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Estado de la Cuenta:</span>
          <span class="info-value">
            <span class="badge-activo">{{ usuario.activo ? 'Activa' : 'Inactiva' }}</span>
          </span>
        </div>
        <div class="info-row" v-if="usuario.fecha_creacion">
          <span class="info-label">Miembro desde:</span>
          <span class="info-value">{{ formatearFecha(usuario.fecha_creacion) }}</span>
        </div>

        <div class="perfil-actions">
          <router-link to="/mis-prestamos" class="btn-mis-prestamos" v-if="usuario.rol !== 'admin'">
            🔖 Ver mis préstamos
          </router-link>
          <router-link to="/prestamos" class="btn-mis-prestamos" v-else>
            📋 Administrar préstamos
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiService from '@/services/api'

export default {
  name: 'PerfilUsuario',
  setup() {
    const usuario = ref(null)
    const cargando = ref(true)

    const cargarPerfil = async () => {
      cargando.value = true
      try {
        usuario.value = await apiService.get('/usuarios/me')
        if (usuario.value) {
          localStorage.setItem('user_role', usuario.value.rol)
          localStorage.setItem('user_name', usuario.value.nombre)
          localStorage.setItem('user_email', usuario.value.email)
        }
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al cargar perfil')
      } finally {
        cargando.value = false
      }
    }

    const formatearFecha = (fechaStr) => {
      if (!fechaStr) return '-'
      const d = new Date(fechaStr)
      return d.toLocaleDateString('es-CO', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      })
    }

    onMounted(cargarPerfil)

    return {
      usuario,
      cargando,
      formatearFecha
    }
  }
}
</script>

<style scoped>
.perfil-usuario {
  max-width: 550px;
  margin: 1.5rem auto;
}

.perfil-card {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  border: 1px solid #e2e8f0;
}

.perfil-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 2rem;
}

.avatar-circle {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
}

.perfil-header h2 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.role-tag {
  font-size: 0.8rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: 700;
}

.tag-admin {
  background: #fef3c7;
  color: #92400e;
}

.tag-user {
  background: #e0f2fe;
  color: #0369a1;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f1f5f9;
}

.info-label {
  color: #64748b;
  font-size: 0.9rem;
}

.info-value {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.badge-activo {
  background: #d4efdf;
  color: #1e8449;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.perfil-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

.btn-mis-prestamos {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.7rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.btn-mis-prestamos:hover {
  background: #2980b9;
}

.loading {
  text-align: center;
  color: #64748b;
  padding: 2rem;
}
</style>
