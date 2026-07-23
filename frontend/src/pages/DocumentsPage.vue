<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useDocumentStore } from '@/stores/documents'
import AppHeader from '@/components/AppHeader.vue'

const store = useDocumentStore()
const isUploading = ref(false)
const error = ref('')

onMounted(() => {
  store.fetchDocuments()
})

async function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]

  if (!file) {
    return
  }

  error.value = ''
  isUploading.value = true

  try {
    await store.uploadDocument(file)
  } catch {
    error.value = 'Fayl yuklashda xatolik yuz berdi'
  } finally {
    isUploading.value = false
    input.value = ''
  }
}

const statusLabels: Record<string, string> = {
  uploaded: 'Yuklandi',
  processing: 'Qayta ishlanmoqda',
  ready: 'Tayyor',
  failed: 'Xatolik',
}

const statusClasses: Record<string, string> = {
  uploaded: 'bg-gray-100 text-gray-700',
  processing: 'bg-yellow-100 text-yellow-700',
  ready: 'bg-green-100 text-green-700',
  failed: 'bg-red-100 text-red-700',
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="mx-auto max-w-3xl px-6 py-10">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold text-gray-900">Hujjatlarim</h2>

        <label
          class="cursor-pointer rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-purple-700"
          :class="{ 'pointer-events-none opacity-50': isUploading }"
        >
          {{ isUploading ? 'Yuklanmoqda...' : 'Hujjat yuklash' }}
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            class="hidden"
            :disabled="isUploading"
            @change="handleFileChange"
          />
        </label>
      </div>

      <p v-if="error" class="mt-4 text-sm text-red-600">{{ error }}</p>

      <div v-if="store.isLoading" class="mt-8 text-sm text-gray-500">Yuklanmoqda...</div>

      <div
        v-else-if="store.documents.length === 0"
        class="mt-8 rounded-xl border border-dashed border-gray-300 p-10 text-center text-sm text-gray-500"
      >
        Hali hujjat yuklanmagan. Yuqoridagi tugma orqali birinchi hujjatingizni yuklang.
      </div>

      <ul v-else class="mt-6 divide-y divide-gray-200 rounded-xl border border-gray-200 bg-white">
        <li
          v-for="doc in store.documents"
          :key="doc.id"
          class="flex items-center justify-between px-4 py-3"
        >
          <div>
            <p class="text-sm font-medium text-gray-900">{{ doc.filename }}</p>
            <p class="text-xs uppercase text-gray-400">{{ doc.file_type }}</p>
          </div>
          <span :class="['rounded-full px-2.5 py-0.5 text-xs font-medium', statusClasses[doc.status]]">
            {{ statusLabels[doc.status] ?? doc.status }}
          </span>
        </li>
      </ul>
    </main>
  </div>
</template>
