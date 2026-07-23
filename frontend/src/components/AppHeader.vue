<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const initials = computed(() => {
  const name = auth.user?.full_name ?? ''
  return (
    name
      .split(' ')
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join('') || '?'
  )
})

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="sticky top-0 z-10 border-b border-gray-200 bg-white/80 backdrop-blur">
    <div class="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
      <div class="flex items-center gap-8">
        <RouterLink to="/" class="flex items-center gap-2">
          <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-indigo-600 text-sm font-bold text-white">
            D
          </span>
          <span class="text-base font-semibold tracking-tight text-gray-900">DocMind AI</span>
        </RouterLink>

        <nav class="flex gap-1 text-sm font-medium text-gray-500">
          <RouterLink
            to="/"
            class="rounded-full px-3 py-1.5 transition hover:bg-gray-100 hover:text-gray-900"
            active-class="!bg-purple-50 !text-purple-700"
          >
            Bosh sahifa
          </RouterLink>
          <RouterLink
            to="/documents"
            class="rounded-full px-3 py-1.5 transition hover:bg-gray-100 hover:text-gray-900"
            active-class="!bg-purple-50 !text-purple-700"
          >
            Hujjatlar
          </RouterLink>
        </nav>
      </div>

      <div class="flex items-center gap-3">
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-purple-100 text-xs font-semibold text-purple-700">
          {{ initials }}
        </div>
        <button
          class="text-sm font-medium text-gray-500 transition hover:text-gray-900"
          @click="handleLogout"
        >
          Chiqish
        </button>
      </div>
    </div>
  </header>
</template>
