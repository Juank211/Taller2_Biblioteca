import { mount } from '@vue/test-utils'
import CrearPrestamo from '@/views/prestamos/CrearPrestamo.vue'
import DevolverPrestamo from '@/views/prestamos/DevolverPrestamo.vue'
import apiService from '@/services/apiService'

jest.mock('@/services/apiService')

describe('Prestamos Components', () => {
  describe('CrearPrestamo.vue', () => {
    it('renders form correctly', () => {
      const wrapper = mount(CrearPrestamo)
      expect(wrapper.find('h2').text()).toBe('Crear Préstamo')
      expect(wrapper.findAll('select').length).toBe(2)
      expect(wrapper.findAll('input[type="date"]').length).toBe(2)
    })

    it('validates form', async () => {
      const wrapper = mount(CrearPrestamo)
      await wrapper.setData({ libroId: '1', socioId: '1', fechaPrestamo: '2023-01-01', fechaDevolucion: '2023-01-15' })
      expect(wrapper.vm.validarFormulario()).toBe(true)
    })
  })

  describe('DevolverPrestamo.vue', () => {
    it('renders form correctly', () => {
      const wrapper = mount(DevolverPrestamo)
      expect(wrapper.find('h2').text()).toBe('Devolver Préstamo')
      expect(wrapper.find('input[type="number"]').exists()).toBe(true)
    })

    it('validates form', async () => {
      const wrapper = mount(DevolverPrestamo)
      await wrapper.setData({ prestamoId: '1' })
      expect(wrapper.vm.validarFormulario()).toBe(true)
    })
  })
})
