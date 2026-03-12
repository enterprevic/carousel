<template>
  <div class="min-h-screen bg-[#f5f5f7] flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="flex items-center gap-2.5 justify-center mx-auto mb-5">
          <img src="/visible.png" alt="trendsee" class="w-10 h-10 object-contain" />
          <span class="font-semibold text-[#1B1A25] tracking-tight" style="font-family:'Unbounded',sans-serif;font-size:22px;line-height:1.2;">trendsee</span>
        </div>
        <h1 class="text-2xl font-bold text-[#1c1c1e] tracking-tight">{{ t.loginWelcome }}</h1>
        <p class="text-[#6e6e73] text-sm mt-1.5">{{ t.loginSubtitle }}</p>
      </div>

      <!-- Card -->
      <div
        class="bg-white rounded-2xl border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-7 space-y-5"
      >
        <div class="space-y-1.5">
          <label class="label">{{ t.loginUsername }}</label>
          <input
            ref="usernameRef"
            v-model="username"
            type="text"
            class="input"
            placeholder="your_username"
            autocomplete="username"
            :disabled="loading"
            @keydown.enter="submit"
          />
        </div>

        <div class="space-y-1.5">
          <label class="label">{{ t.loginPassword }}</label>
          <input
            v-model="password"
            type="password"
            class="input"
            placeholder="••••••••"
            autocomplete="current-password"
            :disabled="loading"
            @keydown.enter="submit"
          />
        </div>

        <div v-if="error" class="px-3.5 py-2.5 bg-red-50 border border-red-100 rounded-xl text-sm text-[#ff3b30] text-center">
          {{ error }}
        </div>

        <button
          class="btn-primary w-full py-3 text-[15px]"
          :disabled="loading || !username || !password"
          @click="submit"
        >
          <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span>{{ loading ? t.loginLoading : t.loginButton }}</span>
        </button>
      </div>

      <p class="text-center text-sm text-[#6e6e73] mt-5">
        {{ t.loginNoAccount }}
        <NuxtLink to="/register" class="text-[#0071e3] font-medium hover:underline">{{ t.loginCreateOne }}</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const { login } = useAuth()
const { t } = useLang()

const username = ref("")
const password = ref("")
const loading = ref(false)
const error = ref<string | null>(null)
const usernameRef = ref<HTMLInputElement>()

onMounted(() => {
  nextTick(() => usernameRef.value?.focus())
})

const submit = async () => {
  if (!username.value || !password.value || loading.value) return
  loading.value = true
  error.value = null
  try {
    await login(username.value, password.value)
    navigateTo("/dashboard")
  } catch (e: any) {
    error.value = e?.data?.detail === "Incorrect username or password"
      ? t.value.loginErrorWrong
      : t.value.loginErrorFail
  } finally {
    loading.value = false
  }
}
</script>
