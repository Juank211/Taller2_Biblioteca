import { mount } from '@vue/test-utils'
import ListadoSocios from '@/views/socios/ListadoSocios.vue'
import DetalleSocio from '@/views/socios/DetalleSocio.vue'
import CrearSocio from '@/views/socios/CrearSocio.vue'
import apiService from '@/services/apiService'

jest.mock('@/services/apiService')

describe('Socios Components', () => {
  describe('ListadoSocios.vue', () => {
    it('renders table correctly', async () => {
      const mockSocios = [{ id: 1, nombre: 'Socio 1', email: 'socio1@example.com', activo: true }]
      apiService.get.mockResolvedValue(mockSocios)

      const wrapper = mount(ListadoSocios)
      await wrapper.vm.$nextTick()
      expect(wrapper.findAll('tr').length).toBeGreaterThan(1)
      expect(wrapper.findAll('td').length).toBeGreaterThan(0)
    })
  })

  describe('DetalleSocio.vue', () => {
    it('renders socio details correctly', async () => {
      const mockSocio = { id: 1, nombre: 'Socio 1', email: 'socio1@example.com', activo: true }
      apiService.get.mockResolvedValue(mockSocio)

      const wrapper = mount(DetalleSocio, {
        global: {
          mocks: {
            $route: { params: { id: 1 } }
          }
        }
      })
      await wrapper.vm.$nextTick()
      expect(wrapper.find('h2').text()).toBe('Detalle del Socio')
      expect(wrapper.find('p').text()).toContain('Socio 1')
    })
  })

  describe('CrearSocio.vue', () => {
    it('renders form correctly', () => {
      const wrapper = mount(CrearSocio)
      expect(wrapper.find('h2').text()).toBe('Crear Socio')
      expect(wrapper.findAll('input').length).toBe(2)
      expect(wrapper.find('select').exists()).toBe(true)
    })

    it('validates form', async () => {
      const wrapper = mount(CrearSocio)
      await wrapper.setData({ nombre: 'Socio 1', email: 'socio1@example.com', activo: 'true' })
      expect(wrapper.vm.validarFormulario()).toBe(true)
    })
  })
})