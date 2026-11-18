import { mount } from '@vue/test-utils'
import ListadoUsuarios from '@/views/usuarios/ListadoUsuarios.vue'
import CrearUsuario from '@/views/usuarios/CrearUsuario.vue'
import PerfilUsuario from '@/views/usuarios/PerfilUsuario.vue'
import EliminarUsuario from '@/views/usuarios/EliminarUsuario.vue'
import apiService from '@/services/apiService'

jest.mock('@/services/apiService')

describe('Usuarios Components', () => {
  describe('ListadoUsuarios.vue', () => {
    it('renders table correctly for admin', async () => {
      const mockUsuarios = [{ id: 1, nombre: 'Admin', email: 'admin@example.com', rol: 'admin' }]
      const mockCurrentUser = { rol: 'admin' }
      apiService.get.mockImplementation((url) => {
        if (url === '/usuarios') return mockUsuarios
        if (url === '/usuarios/me') return mockCurrentUser
      })

      const wrapper = mount(ListadoUsuarios)
      await wrapper.vm.$nextTick()
      expect(wrapper.findAll('tr').length).toBeGreaterThan(1)
      expect(wrapper.findAll('button.btn-eliminar').length).toBeGreaterThan(0)
    })

    it('hides admin options for non-admin', async () => {
      const mockUsuarios = [{ id: 1, nombre: 'User', email: 'user@example.com', rol: 'user' }]
      const mockCurrentUser = { rol: 'user' }
      apiService.get.mockImplementation((url) => {
        if (url === '/usuarios') return mockUsuarios
        if (url === '/usuarios/me') return mockCurrentUser
      })

      const wrapper = mount(ListadoUsuarios)
      await wrapper.vm.$nextTick()
      expect(wrapper.findAll('button.btn-eliminar').length).toBe(0)
    })
  })

  describe('CrearUsuario.vue', () => {
    it('renders form correctly', () => {
      const wrapper = mount(CrearUsuario)
      expect(wrapper.find('h2').text()).toBe('Crear Usuario')
      expect(wrapper.findAll('input').length).toBe(3)
      expect(wrapper.find('select').exists()).toBe(true)
    })

    it('validates form', async () => {
      const wrapper = mount(CrearUsuario)
      await wrapper.setData({ nombre: 'User', email: 'user@example.com', password: 'password', rol: 'user' })
      expect(wrapper.vm.validarFormulario()).toBe(true)
    })
  })

  describe('PerfilUsuario.vue', () => {
    it('renders user profile correctly', async () => {
      const mockUsuario = { id: 1, nombre: 'User', email: 'user@example.com', rol: 'user' }
      apiService.get.mockResolvedValue(mockUsuario)

      const wrapper = mount(PerfilUsuario)
      await wrapper.vm.$nextTick()
      expect(wrapper.find('h2').text()).toBe('Mi Perfil')
      expect(wrapper.find('p').text()).toContain('User')
    })
  })

  describe('EliminarUsuario.vue', () => {
    it('renders form correctly', () => {
      const wrapper = mount(EliminarUsuario)
      expect(wrapper.find('h2').text()).toBe('Eliminar Usuario')
      expect(wrapper.find('input[type="number"]').exists()).toBe(true)
    })

    it('validates form', async () => {
      const wrapper = mount(EliminarUsuario)
      await wrapper.setData({ usuarioId: '1' })
      expect(wrapper.vm.validarFormulario()).toBe(true)
    })
  })
})