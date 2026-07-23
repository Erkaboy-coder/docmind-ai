import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api/client'

export interface DocumentItem {
  id: number
  filename: string
  file_type: string
  status: string
  created_at: string
}

export const useDocumentStore = defineStore('documents', () => {
  const documents = ref<DocumentItem[]>([])
  const isLoading = ref(false)

  async function fetchDocuments() {
    isLoading.value = true

    try {
      const { data } = await apiClient.get<DocumentItem[]>('/documents')
      documents.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function uploadDocument(file: File) {
    const formData = new FormData()
    formData.append('file', file)

    const { data } = await apiClient.post<DocumentItem>('/documents', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    documents.value.unshift(data)

    return data
  }

  async function deleteDocument(documentId: number) {
    await apiClient.delete(`/documents/${documentId}`)
    documents.value = documents.value.filter((doc) => doc.id !== documentId)
  }

  return {
    documents,
    isLoading,
    fetchDocuments,
    uploadDocument,
    deleteDocument,
  }
})
