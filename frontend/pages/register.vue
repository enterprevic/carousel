<template>
  <div class="min-h-screen bg-[#f5f5f7] flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="flex items-center gap-2.5 justify-center mx-auto mb-5">
          <img src="/visible.png" alt="trendsee" class="w-10 h-10 object-contain" />
          <span class="font-semibold text-[#1B1A25] tracking-tight" style="font-family:'Unbounded',sans-serif;font-size:22px;line-height:1.2;">trendsee</span>
        </div>
        <h1 class="text-2xl font-bold text-[#1c1c1e] tracking-tight">{{ t.registerTitle }}</h1>
        <p class="text-[#6e6e73] text-sm mt-1.5">{{ t.registerSubtitle }}</p>
      </div>

      <!-- Card -->
      <div
        class="bg-white rounded-2xl border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-7 space-y-5"
      >
        <div class="space-y-1.5">
          <label class="label">{{ t.registerUsername }}</label>
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
          <p class="text-[11px] text-[#8e8e93] mt-1">{{ t.registerUsernameHint }}</p>
        </div>

        <div class="space-y-1.5">
          <label class="label">{{ t.registerPassword }}</label>
          <input
            v-model="password"
            type="password"
            class="input"
            placeholder="••••••••"
            autocomplete="new-password"
            :disabled="loading"
            @keydown.enter="submit"
          />
          <p class="text-[11px] text-[#8e8e93] mt-1">{{ t.registerPasswordHint }}</p>
        </div>

        <div class="space-y-1.5">
          <label class="label">{{ t.registerConfirm }}</label>
          <input
            v-model="confirm"
            type="password"
            class="input"
            placeholder="••••••••"
            autocomplete="new-password"
            :disabled="loading"
            @keydown.enter="submit"
          />
        </div>

        <div v-if="error" class="px-3.5 py-2.5 bg-red-50 border border-red-100 rounded-xl text-sm text-[#ff3b30] text-center">
          {{ error }}
        </div>

        <button
          class="btn-primary w-full py-3 text-[15px]"
          :disabled="loading || !canSubmit"
          @click="submit"
        >
          <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span>{{ loading ? t.registerLoading : t.registerButton }}</span>
        </button>
      </div>

      <p class="text-center text-sm text-[#6e6e73] mt-5">
        {{ t.registerHaveAccount }}
        <NuxtLink to="/login" class="text-[#0071e3] font-medium hover:underline">{{ t.registerSignIn }}</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const { register } = useAuth()
const { t } = useLang()

const username = ref("")
const password = ref("")
const confirm = ref("")
const loading = ref(false)
const error = ref<string | null>(null)
const usernameRef = ref<HTMLInputElement>()

onMounted(() => {
  nextTick(() => usernameRef.value?.focus())
})

const canSubmit = computed(() =>
  username.value.length >= 3 && password.value.length >= 6 && confirm.value.length > 0
)

const submit = async () => {
  if (!canSubmit.value || loading.value) return
  error.value = null

  if (password.value !== confirm.value) {
    error.value = t.value.registerErrorMismatch
    return
  }

  loading.value = true
  try {
    await register(username.value, password.value)
    navigateTo("/dashboard")
  } catch (e: any) {
    const detail = e?.data?.detail ?? ""
    error.value = detail === "Username already taken"
      ? t.value.registerErrorTaken
      : t.value.registerErrorFail
  } finally {
    loading.value = false
  }
}
</script>
