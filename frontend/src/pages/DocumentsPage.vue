<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDocumentStore } from '@/stores/documents'
import { useChatStore } from '@/stores/chat'
import AppHeader from '@/components/AppHeader.vue'

const router = useRouter()
const store = useDocumentStore()
const chatStore = useChatStore()
const isUploading = ref(false)
const startingChatFor = ref<number | null>(null)
const deletingId = ref<number | null>(null)
const error = ref('')

async function handleStartChat(documentId: number) {
  startingChatFor.value = documentId

  try {
    const chat = await chatStore.openOrCreateChat(documentId)
    router.push({ name: 'chat', params: { documentId, chatId: chat.id } })
  } catch {
    error.value = 'Suhbat boshlashda xatolik yuz berdi'
  } finally {
    startingChatFor.value = null
  }
}

async function handleDelete(documentId: number, filename: string) {
  if (!confirm(`"${filename}" hujjatini o'chirmoqchimisiz? Bu suhbatlarni ham o'chiradi.`)) {
    return
  }

  deletingId.value = documentId

  try {
    await store.deleteDocument(documentId)
  } catch {
    error.value = "Hujjatni o'chirishda xatolik yuz berdi"
  } finally {
    deletingId.value = null
  }
}

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

function formatDate(value: string) {
  const date = new Date(value)
  return `${String(date.getDate()).padStart(2, '0')}.${String(date.getMonth() + 1).padStart(2, '0')}.${date.getFullYear()}`
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

const fileTypeClasses: Record<string, string> = {
  pdf: 'bg-red-50 text-red-600',
  docx: 'bg-blue-50 text-blue-600',
  txt: 'bg-gray-100 text-gray-600',
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-purple-50/60 via-white to-white">
    <AppHeader />

    <main class="mx-auto max-w-5xl px-6 py-12">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-semibold tracking-tight text-gray-900">Hujjatlarim</h2>
          <p class="mt-1 text-sm text-gray-500">PDF, DOCX yoki TXT fayllaringizni boshqaring</p>
        </div>

        <label
          class="inline-flex cursor-pointer items-center gap-2 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:brightness-105"
          :class="{ 'pointer-events-none opacity-50': isUploading }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="h-4 w-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z" />
          </svg>
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
        class="mt-10 flex flex-col items-center rounded-3xl border border-dashed border-gray-300 bg-white/50 px-6 py-16 text-center"
      >
        <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-purple-100 text-purple-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-7 w-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z" />
          </svg>
        </div>
        <h3 class="mt-4 text-base font-semibold text-gray-900">Hali hujjat yuklanmagan</h3>
        <p class="mt-1 max-w-sm text-sm text-gray-500">
          Yuqoridagi tugma orqali birinchi PDF, DOCX yoki TXT hujjatingizni yuklang va AI bilan
          suhbatni boshlang.
        </p>
      </div>

      <ul v-else class="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <li
          v-for="doc in store.documents"
          :key="doc.id"
          class="flex flex-col rounded-2xl border border-gray-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-purple-200 hover:shadow-md"
        >
          <div class="flex items-start gap-3">
            <div
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-xs font-bold uppercase"
              :class="fileTypeClasses[doc.file_type] ?? 'bg-gray-100 text-gray-600'"
            >
              {{ doc.file_type }}
            </div>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-medium text-gray-900">{{ doc.filename }}</p>
              <p class="mt-0.5 text-xs text-gray-400">{{ formatDate(doc.created_at) }}</p>
            </div>
            <span :class="['shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium', statusClasses[doc.status]]">
              {{ statusLabels[doc.status] ?? doc.status }}
            </span>
            <button
              :disabled="deletingId === doc.id"
              class="shrink-0 rounded-lg p-1.5 text-gray-400 transition hover:bg-red-50 hover:text-red-600 disabled:opacity-50"
              aria-label="Hujjatni o'chirish"
              @click="handleDelete(doc.id, doc.filename)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
              </svg>
            </button>
          </div>

          <button
            v-if="doc.status === 'ready'"
            :disabled="startingChatFor === doc.id"
            class="mt-4 inline-flex items-center justify-center gap-1.5 self-start rounded-full bg-purple-50 px-3.5 py-1.5 text-xs font-semibold text-purple-700 transition hover:bg-purple-100 disabled:opacity-50"
            @click="handleStartChat(doc.id)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="h-3.5 w-3.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
            </svg>
            {{ startingChatFor === doc.id ? 'Ochilmoqda...' : 'Suhbat boshlash' }}
          </button>
        </li>
      </ul>
    </main>
  </div>
</template>
