<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="flex items-center justify-between border-b border-gray-200 bg-white px-6 py-4">
    <div class="flex items-center gap-6">
      <h1 class="text-lg font-semibold text-gray-900">DocMind AI</h1>
      <nav class="flex gap-4 text-sm font-medium text-gray-500">
        <RouterLink to="/" class="hover:text-gray-900" active-class="text-purple-600">
          Bosh sahifa
        </RouterLink>
        <RouterLink to="/documents" class="hover:text-gray-900" active-class="text-purple-600">
          Hujjatlar
        </RouterLink>
      </nav>
    </div>

    <button class="text-sm font-medium text-gray-500 hover:text-gray-900" @click="handleLogout">
      Chiqish
    </button>
  </header>
</template>
