<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/AppHeader.vue'

const auth = useAuthStore()

onMounted(() => {
  if (!auth.user) {
    auth.fetchCurrentUser()
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="mx-auto max-w-3xl px-6 py-10">
      <h2 class="text-xl font-semibold text-gray-900">
        Xush kelibsiz{{ auth.user ? `, ${auth.user.full_name}` : '' }}!
      </h2>
      <p class="mt-2 text-sm text-gray-500">
        Hujjatlaringizni yuklab, AI bilan suhbat orqali ulardan foydalanishni boshlang.
      </p>

      <RouterLink
        to="/documents"
        class="mt-6 inline-block rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-purple-700"
      >
        Hujjatlarga o'tish
      </RouterLink>
    </main>
  </div>
</template>
