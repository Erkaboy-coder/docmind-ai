<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PasswordInput from '@/components/PasswordInput.vue'

const router = useRouter()
const auth = useAuthStore()

const error = ref('')
const isLoading = ref(false)

async function handleSubmit(event: Event) {
  const formData = new FormData(event.target as HTMLFormElement)
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  error.value = ''
  isLoading.value = true

  try {
    await auth.login(email, password)
    router.push({ name: 'dashboard' })
  } catch {
    error.value = "Email yoki parol noto'g'ri"
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-sm space-y-6 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
      <div>
        <h1 class="text-2xl font-semibold text-gray-900">DocMind AI</h1>
        <p class="mt-1 text-sm text-gray-500">Hisobingizga kiring</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700" for="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            autocomplete="email"
            placeholder="email@example.com"
            required
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500"
          />
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700" for="password">Parol</label>
          <PasswordInput
            id="password"
            name="password"
            autocomplete="current-password"
            placeholder="Parolingizni kiriting"
            required
          />
        </div>

        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-purple-700 disabled:opacity-50"
        >
          {{ isLoading ? 'Kirilmoqda...' : 'Kirish' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500">
        Akkauntingiz yo'qmi?
        <RouterLink to="/register" class="font-medium text-purple-600 hover:underline">
          Ro'yxatdan o'ting
        </RouterLink>
      </p>
    </div>
  </div>
</template>
