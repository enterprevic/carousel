<template>
  <div class="flex h-screen overflow-hidden bg-[#F4F5F6] relative">
    <AppSidebar :open="isMobile ? mobileSidebarOpen : sidebarOpen" :mobile="isMobile" @toggle="toggle" />

    <div class="flex-1 min-h-0 flex flex-col overflow-hidden">
      <!-- Desktop sidebar reopen button (only shown when sidebar is collapsed) -->
      <button
        v-if="!isMobile && !sidebarOpen"
        class="absolute top-3 left-3 z-30 w-7 h-7 flex items-center justify-center text-[#83939C] hover:text-[#4E616B] hover:bg-[#E6E8EA] rounded-lg transition-colors"
        @click="toggle"
      >
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>
      <!-- Mobile top bar -->
      <div v-if="isMobile" class="shrink-0 h-12 bg-white border-b border-[#E6E8EA] flex items-center px-4 gap-3">
        <NuxtLink to="/dashboard" class="flex items-center gap-[6px] select-none flex-1">
          <img src="/visible.png" alt="trendsee" class="w-[26px] h-[26px] object-contain shrink-0" />
          <span class="font-semibold text-[#1B1A25] tracking-tight whitespace-nowrap" style="font-family:'Unbounded',sans-serif;font-size:15px;line-height:1.2;">trendsee</span>
          <span class="text-[10px] font-bold text-[#2B31B3] bg-[#D5D6F8] px-1.5 py-0.5 rounded-full tracking-wide whitespace-nowrap">Beta</span>
        </NuxtLink>

        <div class="flex items-center gap-1.5 bg-[#F4F5F6] rounded-lg px-2.5 py-1">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M12 2C12 2 7 8 7 13a5 5 0 0010 0c0-5-5-11-5-11z" fill="#FF8E2C" opacity="0.9"/>
            <path d="M12 8c0 0-2.5 3.5-2.5 5.5a2.5 2.5 0 005 0C14.5 11.5 12 8 12 8z" fill="#FF5C1A"/>
          </svg>
          <span class="text-[12px] font-semibold text-[#4E616B]">{{ tokensUsed.toLocaleString() }}<span class="text-[#A0ADB4] font-normal"> / 50k</span></span>
        </div>

        <div class="w-7 h-7 rounded-[8px] bg-[#2B31B3] flex items-center justify-center text-white text-[12px] font-bold shrink-0">
          {{ initial }}
        </div>

        <button
          class="w-8 h-8 flex items-center justify-center text-[#4E616B] hover:text-[#000] rounded-lg hover:bg-[#F4F5F6] transition-colors"
          @click="mobileSidebarOpen = true"
        >
          <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
      </div>

      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const isMobile = ref(import.meta.client ? window.innerWidth < 768 : false)
const sidebarOpen = ref(!isMobile.value)
const mobileSidebarOpen = ref(false)

onMounted(() => {
  const mq = window.matchMedia('(max-width: 767px)')
  isMobile.value = mq.matches
  sidebarOpen.value = !mq.matches
  mq.addEventListener('change', (e) => {
    isMobile.value = e.matches
    if (!e.matches) sidebarOpen.value = true
  })
})

const toggle = () => {
  if (isMobile.value) mobileSidebarOpen.value = !mobileSidebarOpen.value
  else sidebarOpen.value = !sidebarOpen.value
}

const { getUsername } = useAuth()
const username = import.meta.client ? getUsername() : ''
const initial = computed(() => username?.[0]?.toUpperCase() ?? '?')

const tokensUsed = ref(0)
</script>
