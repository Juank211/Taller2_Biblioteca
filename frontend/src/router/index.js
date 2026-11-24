import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import ListadoLibros from '@/views/libros/ListadoLibros.vue'
import CrearLibro from '@/views/libros/CrearLibro.vue'
import GestionPrestamos from '@/views/prestamos/GestionPrestamos.vue'
import MisPrestamos from '@/views/prestamos/MisPrestamos.vue'
import CrearPrestamo from '@/views/prestamos/CrearPrestamo.vue'
import DevolverPrestamo from '@/views/prestamos/DevolverPrestamo.vue'
import ListadoUsuarios from '@/views/usuarios/ListadoUsuarios.vue'
import CrearUsuario from '@/views/usuarios/CrearUsuario.vue'
import PerfilUsuario from '@/views/usuarios/PerfilUsuario.vue'
import EliminarUsuario from '@/views/usuarios/EliminarUsuario.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/registro',
    name: 'register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/libros',
    name: 'listadoLibros',
    component: ListadoLibros
  },
  {
    path: '/libros/crear',
    name: 'crearLibro',
    component: CrearLibro,
    meta: { requiresAdmin: true }
  },
  {
    path: '/prestamos',
    name: 'gestionPrestamos',
    component: GestionPrestamos,
    meta: { requiresAdmin: true }
  },
  {
    path: '/prestamos/crear',
    name: 'crearPrestamo',
    component: CrearPrestamo,
    meta: { requiresAdmin: true }
  },
  {
    path: '/prestamos/devolver/:prestamoId',
    name: 'devolverPrestamo',
    component: DevolverPrestamo
  },
  {
    path: '/mis-prestamos',
    name: 'misPrestamos',
    component: MisPrestamos
  },
  {
    path: '/usuarios',
    name: 'listadoUsuarios',
    component: ListadoUsuarios,
    meta: { requiresAdmin: true }
  },
  {
    path: '/usuarios/crear',
    name: 'crearUsuario',
    component: CrearUsuario,
    meta: { requiresAdmin: true }
  },
  {
    path: '/usuarios/me',
    name: 'perfilUsuario',
    component: PerfilUsuario
  },
  {
    path: '/usuarios/eliminar/:usuarioId',
    name: 'eliminarUsuario',
    component: EliminarUsuario,
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guardia de navegación para proteger rutas y verificar RBAC
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role') || 'usuario'
  const rutasPublicas = ['/login', '/registro']
  const requiereAutenticacion = !rutasPublicas.includes(to.path)

  if (requiereAutenticacion && !token) {
    return next('/login')
  }

  if (token && rutasPublicas.includes(to.path)) {
    return next('/dashboard')
  }

  // Verificación de RBAC para rutas exclusivas de Administrador
  if (to.meta.requiresAdmin && userRole !== 'admin') {
    alert('Acceso restringido: Esta función requiere privilegios de Administrador.')
    return next('/dashboard')
  }

  next()
})

export default router
