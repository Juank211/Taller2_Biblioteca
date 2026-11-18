import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import ListadoLibros from '@/views/libros/ListadoLibros.vue'
import CrearLibro from '@/views/libros/CrearLibro.vue'
import CrearPrestamo from '@/views/prestamos/CrearPrestamo.vue'
import DevolverPrestamo from '@/views/prestamos/DevolverPrestamo.vue'
import ListadoSocios from '@/views/socios/ListadoSocios.vue'
import DetalleSocio from '@/views/socios/DetalleSocio.vue'
import CrearSocio from '@/views/socios/CrearSocio.vue'
import ListadoUsuarios from '@/views/usuarios/ListadoUsuarios.vue'
import CrearUsuario from '@/views/usuarios/CrearUsuario.vue'
import PerfilUsuario from '@/views/usuarios/PerfilUsuario.vue'
import EliminarUsuario from '@/views/usuarios/EliminarUsuario.vue'

const routes = [
  {
    path: '/',
    redirect: '/libros'
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
    path: '/libros',
    name: 'listadoLibros',
    component: ListadoLibros
  },
  {
    path: '/libros/crear',
    name: 'crearLibro',
    component: CrearLibro
  },
  {
    path: '/prestamos/crear',
    name: 'crearPrestamo',
    component: CrearPrestamo
  },
  {
    path: '/prestamos/devolver/:prestamoId',
    name: 'devolverPrestamo',
    component: DevolverPrestamo
  },
  {
    path: '/socios',
    name: 'listadoSocios',
    component: ListadoSocios
  },
  {
    path: '/socios/:socioId',
    name: 'detalleSocio',
    component: DetalleSocio
  },
  {
    path: '/socios/crear',
    name: 'crearSocio',
    component: CrearSocio
  },
  {
    path: '/usuarios',
    name: 'listadoUsuarios',
    component: ListadoUsuarios
  },
  {
    path: '/usuarios/crear',
    name: 'crearUsuario',
    component: CrearUsuario
  },
  {
    path: '/usuarios/me',
    name: 'perfilUsuario',
    component: PerfilUsuario
  },
  {
    path: '/usuarios/eliminar/:usuarioId',
    name: 'eliminarUsuario',
    component: EliminarUsuario
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guardia de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const rutasPublicas = ['/login', '/registro']
  const requiereAutenticacion = !rutasPublicas.includes(to.path)

  if (requiereAutenticacion && !token) {
    return next('/login')
  }

  if (token && rutasPublicas.includes(to.path)) {
    return next('/libros')
  }

  next()
})

export default router;