import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api/client'

export interface ChatItem {
  id: number
  title: string
  document_id: number
  created_at: string
}

export interface MessageItem {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export const useChatStore = defineStore('chat', () => {
  const chats = ref<ChatItem[]>([])
  const messages = ref<MessageItem[]>([])
  const isLoadingChats = ref(false)
  const isLoadingMessages = ref(false)
  const isSending = ref(false)

  async function fetchChats(documentId: number) {
    isLoadingChats.value = true

    try {
      const { data } = await apiClient.get<ChatItem[]>(`/documents/${documentId}/chats`)
      chats.value = data
    } finally {
      isLoadingChats.value = false
    }
  }

  async function createChat(documentId: number) {
    const { data } = await apiClient.post<ChatItem>(`/documents/${documentId}/chats`)
    chats.value.unshift(data)
    return data
  }

  async function openOrCreateChat(documentId: number) {
    await fetchChats(documentId)

    if (chats.value.length > 0) {
      return chats.value[0]
    }

    return await createChat(documentId)
  }

  async function deleteChat(chatId: number) {
    await apiClient.delete(`/chats/${chatId}`)
    chats.value = chats.value.filter((chat) => chat.id !== chatId)
  }

  async function fetchMessages(chatId: number) {
    isLoadingMessages.value = true

    try {
      const { data } = await apiClient.get<MessageItem[]>(`/chats/${chatId}/messages`)
      messages.value = data
    } finally {
      isLoadingMessages.value = false
    }
  }

  async function sendMessage(chatId: number, content: string) {
    messages.value.push({
      id: -Date.now(),
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    })

    isSending.value = true

    try {
      const { data } = await apiClient.post<{ message: MessageItem; sources: string[] }>(
        `/chats/${chatId}/messages`,
        { content }
      )
      messages.value.push(data.message)

      const chat = chats.value.find((c) => c.id === chatId)
      if (chat && chat.title === 'Yangi suhbat') {
        chat.title = content.slice(0, 60)
      }

      return data
    } finally {
      isSending.value = false
    }
  }

  return {
    chats,
    messages,
    isLoadingChats,
    isLoadingMessages,
    isSending,
    fetchChats,
    createChat,
    openOrCreateChat,
    deleteChat,
    fetchMessages,
    sendMessage,
  }
})
