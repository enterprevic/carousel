<template>
  <div class="flex-1 overflow-y-auto">
    <main class="max-w-2xl mx-auto px-8 py-8 space-y-4">
      <h1 class="text-2xl font-bold text-[#000000] tracking-tight mb-6">{{ t.profileTitle }}</h1>
      <!-- User card -->
      <div class="card p-6">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-16 h-16 rounded-2xl bg-[#2B31B3] flex items-center justify-center text-white text-2xl font-bold select-none shrink-0">
            {{ initial }}
          </div>
          <div>
            <div v-if="user" class="text-lg font-bold text-[#000000]">{{ user.username }}</div>
            <div v-else class="h-5 w-32 bg-[#e5e5ea] rounded-lg animate-pulse mb-1" />
            <div v-if="user" class="text-sm text-[#8e8e93]">{{ t.profileMemberSince }} {{ joinDate }}</div>
            <div v-else class="h-4 w-24 bg-[#e5e5ea] rounded-lg animate-pulse" />
          </div>
        </div>

        <div class="border-t border-black/[0.06] pt-5 space-y-3">
          <div class="flex justify-between items-center text-sm">
            <span class="text-[#3a3a3c]">{{ t.profileUsername }}</span>
            <span class="font-medium text-[#000000]">{{ user?.username ?? '…' }}</span>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-[#3a3a3c]">{{ t.profileAccountId }}</span>
            <span class="font-mono text-xs text-[#8e8e93]">{{ user?.id?.slice(0, 8) ?? '…' }}</span>
          </div>
        </div>
      </div>

      <!-- Usage stats -->
      <div class="card p-6">
        <h2 class="font-semibold text-[#000000] mb-4">{{ t.profileUsage }}</h2>
        <div class="grid grid-cols-3 gap-3">
          <!-- Carousels -->
          <div class="rounded-xl bg-[#F4F5F6] px-4 py-4 text-center">
            <p v-if="stats" class="text-[26px] font-black text-[#2B31B3] tracking-tight leading-none">
              {{ stats.carousels }}
            </p>
            <div v-else class="h-7 w-10 bg-[#e5e5ea] rounded-lg animate-pulse mx-auto mb-1" />
            <p class="text-[11px] text-[#6e6e73] mt-1.5 font-medium">{{ t.profileCarousels }}</p>
          </div>
          <!-- Generations -->
          <div class="rounded-xl bg-[#F4F5F6] px-4 py-4 text-center">
            <p v-if="stats" class="text-[26px] font-black text-[#914CFF] tracking-tight leading-none">
              {{ stats.generations }}
            </p>
            <div v-else class="h-7 w-10 bg-[#e5e5ea] rounded-lg animate-pulse mx-auto mb-1" />
            <p class="text-[11px] text-[#6e6e73] mt-1.5 font-medium">{{ t.profileGenerations }}</p>
          </div>
          <!-- Tokens -->
          <div class="rounded-xl bg-[#F4F5F6] px-4 py-4 text-center">
            <p v-if="stats" class="text-[26px] font-black text-[#FF8E2C] tracking-tight leading-none">
              {{ formatTokens(stats.tokens_used) }}
            </p>
            <div v-else class="h-7 w-12 bg-[#e5e5ea] rounded-lg animate-pulse mx-auto mb-1" />
            <p class="text-[11px] text-[#6e6e73] mt-1.5 font-medium">{{ t.profileTokensUsed }}</p>
          </div>
        </div>
        <p v-if="stats" class="text-[11px] text-[#aeaeb2] mt-3 text-center">
          ~{{ formatTokens(stats.tokens_used) }} tokens · approx ${{ approxCost(stats.tokens_used) }} at Groq free tier
        </p>
      </div>

      <!-- Change password -->
      <div class="card p-6">
        <h2 class="font-semibold text-[#000000] mb-4">{{ t.profileChangePw }}</h2>
        <div class="space-y-3">
          <div>
            <label class="label">{{ t.profileCurrentPw }}</label>
            <input v-model="currentPw" type="password" class="input" placeholder="••••••••"
              autocomplete="current-password" :disabled="pwLoading" />
          </div>
          <div>
            <label class="label">{{ t.profileNewPw }}</label>
            <input v-model="newPw" type="password" class="input" placeholder="••••••••"
              autocomplete="new-password" :disabled="pwLoading" />
          </div>
          <div>
            <label class="label">{{ t.profileConfirmPw }}</label>
            <input v-model="confirmPw" type="password" class="input" placeholder="••••••••"
              autocomplete="new-password" :disabled="pwLoading" />
          </div>
          <div v-if="pwError" class="text-sm text-[#ff3b30]">{{ pwError }}</div>
          <div v-if="pwSuccess" class="text-sm text-[#34c759]">{{ t.profilePwSuccess }}</div>
          <button class="btn-primary w-full py-2.5 mt-1" :disabled="pwLoading || !canChangePw" @click="changePassword">
            <svg v-if="pwLoading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span>{{ pwLoading ? t.profileSaving : t.profileSaveBtn }}</span>
          </button>
        </div>
      </div>

      <!-- Sign out -->
      <div class="card p-6">
        <h2 class="font-semibold text-[#000000] mb-1">{{ t.profileSignOut }}</h2>
        <p class="text-sm text-[#8e8e93] mb-4">{{ t.profileSignOutDesc }}</p>
        <button class="w-full py-2.5 rounded-xl border border-[#ff3b30] text-[#ff3b30] text-sm font-medium
          hover:bg-[#ff3b30]/5 transition-colors" @click="logout">
          {{ t.profileSignOutBtn }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const base = config.public.apiBase
const { authHeaders, logout, getUsername } = useAuth()
const { t } = useLang()

interface UserInfo { id: string; username: string; created_at: string }
const user = ref<UserInfo | null>(null)

const initial = computed(() => (user.value?.username ?? getUsername())?.[0]?.toUpperCase() ?? '?')
const joinDate = computed(() => {
  if (!user.value) return ''
  return new Date(user.value.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
})

interface Stats { carousels: number; generations: number; tokens_used: number }
const stats = ref<Stats | null>(null)

const formatTokens = (n: number) => {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M'
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'k'
  return String(n)
}

// Groq free tier pricing is effectively $0 for most usage — show a minimal estimate
// Using ~$0.05 / 1M tokens as a rough reference
const approxCost = (n: number) => (n * 0.00000005).toFixed(4)

onMounted(async () => {
  try {
    const [u, s] = await Promise.all([
      $fetch<UserInfo>(`${base}/auth/me`, { headers: authHeaders() }),
      $fetch<Stats>(`${base}/auth/me/stats`, { headers: authHeaders() }),
    ])
    user.value = u
    stats.value = s
  } catch {}
})

// Change password
const currentPw = ref('')
const newPw = ref('')
const confirmPw = ref('')
const pwLoading = ref(false)
const pwError = ref<string | null>(null)
const pwSuccess = ref(false)

const canChangePw = computed(() => currentPw.value && newPw.value.length >= 6 && confirmPw.value)

const changePassword = async () => {
  pwError.value = null
  pwSuccess.value = false
  if (newPw.value !== confirmPw.value) { pwError.value = t.value.profilePwErrorMismatch; return }
  pwLoading.value = true
  try {
    await $fetch(`${base}/auth/password`, {
      method: 'POST',
      body: { current_password: currentPw.value, new_password: newPw.value },
      headers: authHeaders(),
    })
    pwSuccess.value = true
    currentPw.value = ''
    newPw.value = ''
    confirmPw.value = ''
  } catch (e: any) {
    pwError.value = e?.data?.detail === 'Incorrect password'
      ? t.value.profilePwErrorWrong
      : t.value.profilePwErrorFail
  } finally {
    pwLoading.value = false
  }
}
</script>
