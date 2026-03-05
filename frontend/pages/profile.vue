<template>
  <div class="min-h-screen bg-[#f2f2f7]">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-black/[0.07]">
      <div class="max-w-2xl mx-auto px-5 sm:px-8 h-14 flex items-center gap-3">
        <NuxtLink to="/dashboard"
          class="w-8 h-8 rounded-xl flex items-center justify-center text-[#3a3a3c] hover:bg-black/5 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </NuxtLink>
        <span class="font-semibold text-[#1c1c1e] text-[15px]">Profile</span>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-5 sm:px-8 py-10 space-y-4">
      <!-- User card -->
      <div class="card p-6">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-16 h-16 rounded-2xl bg-[#0071e3] flex items-center justify-center text-white text-2xl font-bold select-none shrink-0">
            {{ initial }}
          </div>
          <div>
            <div v-if="user" class="text-lg font-bold text-[#1c1c1e]">{{ user.username }}</div>
            <div v-else class="h-5 w-32 bg-[#e5e5ea] rounded-lg animate-pulse mb-1" />
            <div v-if="user" class="text-sm text-[#8e8e93]">Member since {{ joinDate }}</div>
            <div v-else class="h-4 w-24 bg-[#e5e5ea] rounded-lg animate-pulse" />
          </div>
        </div>

        <div class="border-t border-black/[0.06] pt-5 space-y-3">
          <div class="flex justify-between items-center text-sm">
            <span class="text-[#3a3a3c]">Username</span>
            <span class="font-medium text-[#1c1c1e]">{{ user?.username ?? '…' }}</span>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-[#3a3a3c]">Account ID</span>
            <span class="font-mono text-xs text-[#8e8e93]">{{ user?.id?.slice(0, 8) ?? '…' }}</span>
          </div>
        </div>
      </div>

      <!-- Change password -->
      <div class="card p-6">
        <h2 class="font-semibold text-[#1c1c1e] mb-4">Change Password</h2>
        <div class="space-y-3">
          <div>
            <label class="label">Current Password</label>
            <input v-model="currentPw" type="password" class="input" placeholder="••••••••"
              autocomplete="current-password" :disabled="pwLoading" />
          </div>
          <div>
            <label class="label">New Password</label>
            <input v-model="newPw" type="password" class="input" placeholder="••••••••"
              autocomplete="new-password" :disabled="pwLoading" />
          </div>
          <div>
            <label class="label">Confirm New Password</label>
            <input v-model="confirmPw" type="password" class="input" placeholder="••••••••"
              autocomplete="new-password" :disabled="pwLoading" />
          </div>
          <div v-if="pwError" class="text-sm text-[#ff3b30]">{{ pwError }}</div>
          <div v-if="pwSuccess" class="text-sm text-[#34c759]">Password changed successfully.</div>
          <button class="btn-primary w-full py-2.5 mt-1" :disabled="pwLoading || !canChangePw" @click="changePassword">
            <svg v-if="pwLoading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span>{{ pwLoading ? 'Saving…' : 'Change Password' }}</span>
          </button>
        </div>
      </div>

      <!-- Sign out -->
      <div class="card p-6">
        <h2 class="font-semibold text-[#1c1c1e] mb-1">Sign Out</h2>
        <p class="text-sm text-[#8e8e93] mb-4">You'll need to sign back in to access your carousels.</p>
        <button class="w-full py-2.5 rounded-xl border border-[#ff3b30] text-[#ff3b30] text-sm font-medium
          hover:bg-[#ff3b30]/5 transition-colors" @click="logout">
          Sign out
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const base = config.public.apiBase
const { authHeaders, logout, getUsername } = useAuth()

interface UserInfo { id: string; username: string; created_at: string }
const user = ref<UserInfo | null>(null)

const initial = computed(() => (user.value?.username ?? getUsername())?.[0]?.toUpperCase() ?? '?')
const joinDate = computed(() => {
  if (!user.value) return ''
  return new Date(user.value.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
})

onMounted(async () => {
  try {
    user.value = await $fetch<UserInfo>(`${base}/auth/me`, { headers: authHeaders() })
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
  if (newPw.value !== confirmPw.value) { pwError.value = 'New passwords do not match'; return }
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
      ? 'Current password is incorrect'
      : 'Failed to change password. Please try again.'
  } finally {
    pwLoading.value = false
  }
}
</script>
