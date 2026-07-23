<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useDocumentStore } from '@/stores/documents'
import AppHeader from '@/components/AppHeader.vue'

const auth = useAuthStore()
const documentStore = useDocumentStore()

const readyCount = computed(
  () => documentStore.documents.filter((doc) => doc.status === 'ready').length
)

onMounted(() => {
  if (!auth.user) {
    auth.fetchCurrentUser()
  }
  documentStore.fetchDocuments()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-purple-50/60 via-white to-white">
    <AppHeader />

    <main class="mx-auto max-w-5xl px-6 py-12">
      <section class="rounded-3xl bg-gradient-to-br from-purple-600 to-indigo-600 px-8 py-10 text-white shadow-lg shadow-purple-200/60">
        <p class="text-sm font-medium text-purple-100">Xush kelibsiz</p>
        <h2 class="mt-1 text-3xl font-semibold tracking-tight">
          {{ auth.user ? auth.user.full_name : '...' }}
        </h2>
        <p class="mt-3 max-w-xl text-sm text-purple-100">
          Hujjatlaringizni yuklab, AI bilan suhbat orqali ulardan savol-javob, xulosalash va
          tahlil qilishni boshlang.
        </p>

        <RouterLink
          to="/documents"
          class="mt-6 inline-flex items-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-semibold text-purple-700 shadow-sm transition hover:bg-purple-50"
        >
          Hujjatlarga o'tish
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="h-4 w-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
          </svg>
        </RouterLink>
      </section>

      <section class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3">
        <div class="rounded-2xl border border-gray-200 bg-white p-5">
          <p class="text-2xl font-semibold text-gray-900">{{ documentStore.documents.length }}</p>
          <p class="mt-1 text-sm text-gray-500">Yuklangan hujjat</p>
        </div>
        <div class="rounded-2xl border border-gray-200 bg-white p-5">
          <p class="text-2xl font-semibold text-gray-900">{{ readyCount }}</p>
          <p class="mt-1 text-sm text-gray-500">Suhbatga tayyor</p>
        </div>
        <div class="hidden rounded-2xl border border-dashed border-gray-300 bg-white/50 p-5 sm:flex sm:items-center">
          <p class="text-sm text-gray-400">Tez orada: umumiy suhbatlar statistikasi</p>
        </div>
      </section>
    </main>
  </div>
</template>
