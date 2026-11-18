import axios from 'axios'

// Obtener la URL base desde variables de entorno o fallback a localhost
const envBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const apiBaseUrl = envBaseUrl.endsWith('/api/v1') 
  ? envBaseUrl 
  : `${envBaseUrl.replace(/\/$/, '')}/api/v1`

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para inyectar token de autenticación si existe
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Interceptor de respuesta para manejar 401 (token expirado o inválido)
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_email')
      if (window.location.pathname !== '/login' && window.location.pathname !== '/registro') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// Métodos auxiliares
export const apiService = {
  get: async (url, config = {}) => {
    const response = await apiClient.get(url, config)
    return response.data
  },
  post: async (url, data, config = {}) => {
    const response = await apiClient.post(url, data, config)
    return response.data
  },
  put: async (url, data, config = {}) => {
    const response = await apiClient.put(url, data, config)
    return response.data
  },
  delete: async (url, config = {}) => {
    const response = await apiClient.delete(url, config)
    return response.data
  }
}

export default apiService
