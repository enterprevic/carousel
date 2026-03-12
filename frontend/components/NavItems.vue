<template>
  <!-- Поиск контента -->
  <p class="px-2 pt-1 pb-1 text-[11px] font-bold text-[#83939C] uppercase tracking-widest whitespace-nowrap">{{ t.searchContent }}</p>
  <NuxtLink to="/dashboard" :class="itemClass('/dashboard')" @click="$emit('close')">
    <SidebarIcon color="#2B31B3" bg="#EEF0FF">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.home }}</span>
  </NuxtLink>
  <div :class="itemDisabled">
    <!-- Поиск по слову — blue search icon -->
    <SidebarIcon color="#2B63D9" bg="#E8EEFB">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.searchByWord }}</span>
  </div>
  <div :class="itemDisabled">
    <!-- Шпионаж — incognito/spy icon in purple -->
    <SidebarIcon color="#914CFF" bg="#F3E8FF">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.spy }}</span>
  </div>
  <div :class="itemDisabled">
    <!-- Контент-радар — bullseye/target in red -->
    <SidebarIcon color="#E53E3E" bg="#FFF0F0">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
        <circle cx="12" cy="12" r="7" stroke="currentColor" stroke-width="2"/>
        <circle cx="12" cy="12" r="11" stroke="currentColor" stroke-width="2"/>
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.contentRadar }}</span>
    <span class="ml-auto text-[11px] font-bold text-[#2B31B3] bg-[#D5D6F8] px-2 py-0.5 rounded-full whitespace-nowrap">712</span>
  </div>

  <!-- Работа с соцсетями -->
  <p class="px-2 pt-4 pb-1 text-[11px] font-bold text-[#83939C] uppercase tracking-widest whitespace-nowrap">{{ t.socialMedia }}</p>
  <div :class="itemDisabled">
    <!-- Кросс-постинг — share icon with 3 nodes in pink -->
    <SidebarIcon color="#E91E8C" bg="#FDE8F3">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.crossPosting }}</span>
  </div>
  <NuxtLink to="/dashboard" :class="itemClass('/dashboard', true)" @click="$emit('close')">
    <!-- Карусели — carousel/layers icon in light orange -->
    <SidebarIcon color="#FF8E2C" bg="#FFF0E8">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap font-semibold">{{ t.carousels }}</span>
  </NuxtLink>

  <!-- Инструменты -->
  <p class="px-2 pt-4 pb-1 text-[11px] font-bold text-[#83939C] uppercase tracking-widest whitespace-nowrap">{{ t.tools }}</p>
  <div :class="itemDisabled">
    <!-- ИИ-сценарий — wand with stars in teal -->
    <SidebarIcon color="#0D9488" bg="#E6FAF8">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3l1 1M5 3L4 4M5 3l-1-1m2 2l9 9m-4-4l4 4m0 0l2 2m-2-2l2-2m-5 1l1-3 1 3m-4-1l-3 1 3 1" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3l.5 1.5M14 5l1.5.5M12 1v1.5" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.aiScript }}</span>
  </div>
  <NuxtLink to="/carousels/new" :class="itemClass('/carousels/new')" @click="$emit('close')">
    <!-- Новая карусель — same orange carousel icon -->
    <SidebarIcon color="#FF8E2C" bg="#FFF0E8">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.newCarousel }}</span>
  </NuxtLink>
  <div :class="itemDisabled">
    <!-- Анализ видео — link/film icon in purple -->
    <SidebarIcon color="#914CFF" bg="#F3E8FF">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.videoAnalysis }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#F59E0B" bg="#FEF3C7">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.profileAnalysis }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#10B981" bg="#D1FAE5">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.drafts }}</span>
    <span class="ml-auto text-[11px] font-bold text-[#83939C] bg-[#E6E8EA] px-2 py-0.5 rounded-full whitespace-nowrap">{{ t.soon }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#3B82F6" bg="#DBEAFE">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.contentPlan }}</span>
    <span class="ml-auto text-[11px] font-bold text-[#83939C] bg-[#E6E8EA] px-2 py-0.5 rounded-full whitespace-nowrap">{{ t.soon }}</span>
  </div>

  <!-- Идеи -->
  <p class="px-2 pt-4 pb-1 text-[11px] font-bold text-[#83939C] uppercase tracking-widest whitespace-nowrap">{{ t.ideas }}</p>
  <div :class="itemDisabled">
    <SidebarIcon color="#F43F5E" bg="#FFE4E6">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.favorites }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#6366F1" bg="#EEF2FF">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.history }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#D97706" bg="#FEF3C7">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.bookmarks }}</span>
    <span class="ml-auto text-[11px] font-bold text-[#83939C] bg-[#E6E8EA] px-2 py-0.5 rounded-full whitespace-nowrap">{{ t.soon }}</span>
  </div>

  <!-- Ещё -->
  <p class="px-2 pt-4 pb-1 text-[11px] font-bold text-[#83939C] uppercase tracking-widest whitespace-nowrap">{{ t.more }}</p>
  <div :class="itemDisabled">
    <SidebarIcon color="#0EA5E9" bg="#E0F2FE">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.training }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#8B5CF6" bg="#EDE9FE">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.referrals }}</span>
  </div>
  <div :class="itemDisabled">
    <SidebarIcon color="#F97316" bg="#FFEDD5">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.suggestIdea }}</span>
  </div>
  <NuxtLink to="/profile" :class="itemClass('/profile')" @click="$emit('close')">
    <SidebarIcon color="#64748B" bg="#F1F5F9">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    </SidebarIcon>
    <span class="whitespace-nowrap">{{ t.support }}</span>
  </NuxtLink>
</template>

<script setup lang="ts">
import { useLang } from '~/composables/useLang'

defineEmits<{ close: [] }>()

const route = useRoute()
const { t } = useLang()

const itemClass = (path: string, forceActive = false) => {
  const isActive = forceActive || route.path === path || (path !== '/dashboard' && route.path.startsWith(path))
  return [
    'flex items-center gap-[14px] px-2 py-[7px] rounded-[8px] transition-colors cursor-pointer select-none text-[15px] leading-[24px] font-semibold',
    isActive ? 'bg-[#E6E8EA] text-[#000000]' : 'text-[#1a1a1a] hover:bg-[#E6E8EA] hover:text-[#000000]',
  ]
}

const itemDisabled = 'flex items-center gap-[14px] px-2 py-[7px] rounded-[8px] cursor-default select-none text-[15px] leading-[24px] font-semibold text-[#83939C]'
</script>
