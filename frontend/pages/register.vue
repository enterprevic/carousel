<template>
  <div class="min-h-screen bg-[#f5f5f7] flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div
          class="w-16 h-16 bg-[#0071e3] rounded-[22px] flex items-center justify-center mx-auto mb-5 shadow-[0_8px_32px_rgba(0,113,227,0.35)]"
        >
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
            />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-[#1c1c1e] tracking-tight">Create your account</h1>
        <p class="text-[#6e6e73] text-sm mt-1.5">Get started with CarouselGen</p>
      </div>

      <!-- Card -->
      <div
        class="bg-white rounded-2xl border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] p-7 space-y-5"
      >
        <div class="space-y-1.5">
          <label class="label">Username</label>
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
          <p class="text-[11px] text-[#8e8e93] mt-1">3–32 characters, letters, numbers, underscores</p>
        </div>

        <div class="space-y-1.5">
          <label class="label">Password</label>
          <input
            v-model="password"
            type="password"
            class="input"
            placeholder="••••••••"
            autocomplete="new-password"
            :disabled="loading"
            @keydown.enter="submit"
          />
          <p class="text-[11px] text-[#8e8e93] mt-1">Minimum 6 characters</p>
        </div>

        <div class="space-y-1.5">
          <label class="label">Confirm Password</label>
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
          <span>{{ loading ? "Creating account…" : "Create account" }}</span>
        </button>
      </div>

      <p class="text-center text-sm text-[#6e6e73] mt-5">
        Already have an account?
        <NuxtLink to="/login" class="text-[#0071e3] font-medium hover:underline">Sign in</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const { register } = useAuth()

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
    error.value = "Passwords do not match"
    return
  }

  loading.value = true
  try {
    await register(username.value, password.value)
    navigateTo("/dashboard")
  } catch (e: any) {
    const detail = e?.data?.detail ?? ""
    error.value = detail === "Username already taken"
      ? "Username already taken. Please choose another."
      : "Registration failed. Please try again."
  } finally {
    loading.value = false
  }
}
</script>
