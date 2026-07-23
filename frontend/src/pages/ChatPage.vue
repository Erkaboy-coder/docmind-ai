<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import AppHeader from '@/components/AppHeader.vue'

const route = useRoute()
const router = useRouter()
const store = useChatStore()

const documentId = computed(() => Number(route.params.documentId))
const chatId = computed(() => Number(route.params.chatId))

const messagesEnd = ref<HTMLElement | null>(null)
const draft = ref('')
const error = ref('')

async function loadChat() {
  await store.fetchMessages(chatId.value)
  scrollToBottom()
}

async function scrollToBottom() {
  await nextTick()
  messagesEnd.value?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(async () => {
  await store.fetchChats(documentId.value)
  await loadChat()
})

watch(chatId, loadChat)

async function handleNewChat() {
  const chat = await store.createChat(documentId.value)
  router.push({ name: 'chat', params: { documentId: documentId.value, chatId: chat.id } })
}

async function handleSend() {
  const content = draft.value.trim()

  if (!content || store.isSending) {
    return
  }

  draft.value = ''
  error.value = ''
  scrollToBottom()

  try {
    await store.sendMessage(chatId.value, content)
  } catch {
    error.value = "Javob olishda xatolik yuz berdi. Ollama ishlab turganini tekshiring."
  } finally {
    scrollToBottom()
  }
}
</script>

<template>
  <div class="flex h-screen flex-col bg-gray-50">
    <AppHeader />

    <div class="flex min-h-0 flex-1">
      <aside class="flex w-64 flex-col border-r border-gray-200 bg-white">
        <div class="p-3">
          <button
            class="w-full rounded-lg bg-purple-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-purple-700"
            @click="handleNewChat"
          >
            + Yangi suhbat
          </button>
        </div>

        <nav class="flex-1 overflow-y-auto px-2 pb-2">
          <RouterLink
            v-for="chat in store.chats"
            :key="chat.id"
            :to="{ name: 'chat', params: { documentId, chatId: chat.id } }"
            class="block truncate rounded-lg px-3 py-2 text-sm text-gray-600 hover:bg-gray-100"
            active-class="bg-purple-50 text-purple-700 font-medium"
          >
            {{ chat.title }}
          </RouterLink>
        </nav>
      </aside>

      <main class="flex min-h-0 flex-1 flex-col">
        <div class="flex-1 overflow-y-auto px-6 py-6">
          <div class="mx-auto flex max-w-2xl flex-col gap-4">
            <div
              v-for="message in store.messages"
              :key="message.id"
              class="flex"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-lg rounded-2xl px-4 py-2 text-sm"
                :class="
                  message.role === 'user'
                    ? 'bg-purple-600 text-white'
                    : 'bg-white border border-gray-200 text-gray-800'
                "
              >
                {{ message.content }}
              </div>
            </div>

            <div v-if="store.isSending" class="flex justify-start">
              <div class="max-w-lg rounded-2xl border border-gray-200 bg-white px-4 py-2 text-sm text-gray-400">
                Yozmoqda...
              </div>
            </div>

            <div ref="messagesEnd" />
          </div>
        </div>

        <div class="border-t border-gray-200 bg-white px-6 py-4">
          <form class="mx-auto flex max-w-2xl gap-2" @submit.prevent="handleSend">
            <input
              v-model="draft"
              type="text"
              placeholder="Hujjat haqida savol bering..."
              class="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500"
            />
            <button
              type="submit"
              :disabled="store.isSending"
              class="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-purple-700 disabled:opacity-50"
            >
              Yuborish
            </button>
          </form>
          <p v-if="error" class="mx-auto mt-2 max-w-2xl text-sm text-red-600">{{ error }}</p>
        </div>
      </main>
    </div>
  </div>
</template>
