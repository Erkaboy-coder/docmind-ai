import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '@/api/client'

interface User {
  id: number
  full_name: string
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const { data } = await apiClient.post('/login', { email, password })

    token.value = data.access_token
    localStorage.setItem('token', data.access_token)

    await fetchCurrentUser()
  }

  async function register(fullName: string, email: string, password: string) {
    await apiClient.post('/users', {
      full_name: fullName,
      email,
      password,
    })
  }

  async function fetchCurrentUser() {
    const { data } = await apiClient.get<User>('/me')
    user.value = data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    fetchCurrentUser,
    logout,
  }
})
