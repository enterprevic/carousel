<template>
  <!-- ── MOBILE: bottom-sheet modal ── -->
  <template v-if="mobile">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 z-40 bg-black/50" @click="$emit('toggle')" />
    </Transition>

    <Transition name="slide-up">
      <div
        v-if="open"
        class="fixed bottom-0 left-0 right-0 z-50 bg-[#F4F5F6] rounded-t-[16px] flex flex-col overflow-hidden"
        style="max-height: 87vh;"
        @click.stop
      >
        <!-- Token card -->
        <div class="mx-2 mt-6 mb-1 bg-white rounded-[12px] px-4 py-4 shrink-0">
          <div class="flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C12 2 7 8 7 13a5 5 0 0010 0c0-5-5-11-5-11z" fill="#E53E3E" opacity="0.9"/>
                  <path d="M12 8c0 0-2.5 3.5-2.5 5.5a2.5 2.5 0 005 0C14.5 11.5 12 8 12 8z" fill="#C53030"/>
                </svg>
                <span class="text-[14px] font-bold italic text-[#000]">{{ t.tokens }}</span>
              </div>
              <span class="text-[14px] text-[#000]">{{ tokensUsed.toLocaleString() }} / 50 000</span>
            </div>
            <div class="w-full h-2 bg-[#E6E8EA] rounded-full overflow-hidden">
              <div class="h-full bg-[#2B31B3] rounded-full transition-all duration-500" :style="{ width: `${Math.min(tokenPercent, 100)}%` }" />
            </div>
            <div class="flex items-center gap-1">
              <span class="text-[14px] text-[#83939C] font-medium">Creative +</span>
              <svg class="w-4 h-4 text-[#83939C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Nav items -->
        <nav class="flex-1 overflow-y-auto px-2 py-1">
          <!-- Group 1 -->
          <div class="bg-white rounded-[8px] overflow-hidden mb-1">
            <MobileNavRow icon="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" label="AI-сценарий" @click="$emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M4 6h16M4 10h16M4 14h16M4 18h16" label="Карусели" :active="true" @click="navigateTo('/dashboard'); $emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M15 10l4.553-2.069A1 1 0 0121 8.868V15.13a1 1 0 01-1.447.899L15 14M3 8h12a2 2 0 012 2v4a2 2 0 01-2 2H3a2 2 0 01-2-2v-4a2 2 0 012-2z" label="Анализ видео" @click="$emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" label="Анализ профиля" @click="$emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" label="Рефералы" @click="$emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" label="История" @click="$emit('toggle')" />
          </div>

          <!-- Group 2 -->
          <div class="bg-white rounded-[8px] overflow-hidden mb-1">
            <MobileNavRow icon="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" label="Кросс-постинг" @click="$emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" label="Чат боты" @click="$emit('toggle')" />
          </div>

          <!-- Group 3 -->
          <div class="bg-white rounded-[8px] overflow-hidden mb-1">
            <MobileNavRow icon="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" label="Поддержка" @click="navigateTo('/profile'); $emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" label="Предложить идею" @click="$emit('toggle')" />
            <div class="h-px bg-[#F4F5F6] mx-2" />
            <MobileNavRow icon="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" label="Обучение" @click="$emit('toggle')" />
          </div>
        </nav>

        <!-- User + sign out -->
        <div class="mx-2 mb-2 bg-white rounded-[12px] overflow-hidden shrink-0">

        <!-- User row -->
        <div class="px-3 py-3 flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-[#2B31B3] flex items-center justify-center text-white text-[13px] font-bold shrink-0">
            {{ initial }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-[14px] font-medium text-[#4E616B] truncate leading-tight">{{ username }}</p>
          </div>
        </div>

        <!-- Sign out row -->
        <div class="h-px bg-[#F4F5F6]" />
        <button
          class="w-full px-3 py-3 flex items-center gap-4 text-[#4E616B] hover:bg-[#F4F5F6] transition-colors"
          style="padding-bottom: max(12px, env(safe-area-inset-bottom));"
          @click="handleLogout"
        >
          <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          <span class="text-[16px] font-medium">{{ t.signOut }}</span>
        </button>
        </div>
      </div>
    </Transition>
  </template>

  <!-- ── DESKTOP: side panel ── -->
  <template v-else>
    <aside
      class="shrink-0 h-screen bg-[#F4F5F6] border-r border-[#E0E0E0] transition-all duration-300 ease-in-out overflow-hidden flex flex-col"
      :style="{ width: open ? '274px' : '0px', minWidth: open ? '274px' : '0px', visibility: open ? 'visible' : 'hidden' }"
    >
      <!-- Logo -->
      <div class="px-4 pt-3 pb-2 flex items-center justify-between shrink-0" style="min-width:274px">
        <NuxtLink to="/dashboard" class="flex items-center gap-[6px] select-none">
          <img src="/visible.png" alt="trendsee" class="w-[28px] h-[28px] object-contain shrink-0" />
          <span class="font-semibold text-[#1B1A25] tracking-tight whitespace-nowrap" style="font-family:'Unbounded',sans-serif;font-size:17px;line-height:1.2;">trendsee</span>
          <span class="text-[11px] font-bold text-[#2B31B3] bg-[#D5D6F8] px-2 py-0.5 rounded-full tracking-wide whitespace-nowrap">Beta</span>
        </NuxtLink>
        <button class="w-5 h-5 flex items-center justify-center text-[#83939C] hover:text-[#4E616B] transition-colors shrink-0" @click="$emit('toggle')">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
      </div>

      <!-- Nav scroll area -->
      <nav class="flex-1 overflow-y-auto px-4 py-3 flex flex-col" style="min-width:274px">
        <NavItems />
      </nav>

      <!-- Bottom section -->
      <div class="px-4 pb-4 flex flex-col gap-1 shrink-0" style="min-width:274px">
        <!-- Token card -->
        <div class="bg-white rounded-[12px] px-3 py-3 flex flex-col gap-3">
          <div class="flex flex-col gap-2">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C12 2 7 8 7 13a5 5 0 0010 0c0-5-5-11-5-11z" fill="#E53E3E" opacity="0.9"/>
                  <path d="M12 8c0 0-2.5 3.5-2.5 5.5a2.5 2.5 0 005 0C14.5 11.5 12 8 12 8z" fill="#C53030"/>
                </svg>
                <span class="text-[13px] font-bold italic text-[#000000] whitespace-nowrap">{{ t.tokens }}</span>
              </div>
              <span class="text-[13px] text-[#000000] whitespace-nowrap">{{ tokensUsed.toLocaleString() }} / 50 000</span>
            </div>
            <div class="w-full h-2 bg-[#E6E8EA] rounded-full overflow-hidden">
              <div class="h-full bg-[#2B31B3] rounded-full transition-all duration-500"
                :style="{ width: `${Math.min(tokenPercent, 100)}%` }" />
            </div>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-[13px] text-[#83939C] font-medium whitespace-nowrap">{{ t.creativePlus }}</span>
            <svg class="w-5 h-5 text-[#83939C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>

        <!-- User card -->
        <div class="flex items-center gap-2 px-1 py-2 rounded-[12px] hover:bg-[#E6E8EA] transition-colors cursor-pointer select-none"
          @click="handleLogout">
          <div class="w-8 h-8 rounded-[10px] bg-[#2B31B3] flex items-center justify-center text-white text-[13px] font-bold shrink-0">
            {{ initial }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-[13px] font-semibold text-[#4E616B] truncate leading-tight">{{ username }}</p>
            <p class="text-[11px] text-[#A0ADB4] leading-tight whitespace-nowrap">{{ t.signOut }}</p>
          </div>
          <svg class="w-5 h-5 text-[#83939C] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </div>

        <!-- Language selector -->
        <div class="px-2 py-1">
          <select
            :value="lang"
            class="lang-select w-full bg-[#E6E8EA] rounded-[8px] px-2 py-1.5 text-[12px] font-semibold text-[#4E616B] border-none outline-none cursor-pointer"
            @change="setLang(($event.target as HTMLSelectElement).value as 'ru' | 'en')"
          >
            <option value="ru">🇷🇺 Русский</option>
            <option value="en">🇬🇧 English</option>
          </select>
        </div>
      </div>
    </aside>
  </template>
</template>

<script setup lang="ts">
defineProps<{ open: boolean; mobile?: boolean }>()
const emit = defineEmits<{ toggle: [] }>()

const route = useRoute()
const { logout, getUsername, authHeaders } = useAuth()
const { lang, t, setLang } = useLang()

const username = import.meta.client ? getUsername() : ''
const initial = computed(() => username?.[0]?.toUpperCase() ?? '?')

const config = useRuntimeConfig()
const tokensUsed = ref(0)
const tokenPercent = computed(() => Math.min((tokensUsed.value / 50000) * 100, 100))

onMounted(async () => {
  try {
    const stats = await $fetch<{ tokens_used: number }>(`${config.public.apiBase}/auth/me/stats`, {
      headers: authHeaders(),
    })
    tokensUsed.value = stats.tokens_used ?? 0
  } catch {}
})

const itemClass = (path: string, forceActive = false) => {
  const isActive = forceActive || route.path === path || (path !== '/dashboard' && route.path.startsWith(path))
  return [
    'flex items-center gap-[14px] px-2 py-[7px] rounded-[8px] transition-colors cursor-pointer select-none text-[15px] leading-[24px] font-semibold',
    isActive ? 'bg-[#E6E8EA] text-[#000000]' : 'text-[#1a1a1a] hover:bg-[#E6E8EA] hover:text-[#000000]',
  ]
}

const itemDisabled = 'flex items-center gap-[14px] px-2 py-[7px] rounded-[8px] cursor-default select-none text-[15px] leading-[24px] font-semibold text-[#1a1a1a] opacity-40'

const handleLogout = () => logout()
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1); }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }

.lang-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2383939C' stroke-width='2.5'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  padding-right: 24px;
}
</style>
