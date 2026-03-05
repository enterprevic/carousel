<template>
  <div
    class="group relative flex flex-col justify-end overflow-hidden rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] cursor-pointer min-h-[18rem]"
    :class="className"
  >
    <!-- Background slot — sits behind content -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <slot name="background" />
    </div>

    <!-- Spacer so background visuals show above the text -->
    <div class="flex-1" />

    <!-- Content — slides up on hover -->
    <div class="pointer-events-none relative z-10 flex flex-col gap-1 p-6 transition-all duration-300 group-hover:-translate-y-10">
      <div class="h-12 w-12 mb-1 origin-left transform-gpu transition-all duration-300 ease-in-out group-hover:scale-75">
        <slot name="icon" />
      </div>
      <h3 class="text-[17px] font-semibold text-[#1c1c1e]">{{ name }}</h3>
      <p class="text-[13px] text-[#8e8e93] leading-relaxed max-w-sm">{{ description }}</p>
    </div>

    <!-- CTA — revealed on hover -->
    <div class="pointer-events-none absolute bottom-0 left-0 right-0 flex translate-y-10 items-center p-4 opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100 z-10">
      <NuxtLink :to="href"
        class="pointer-events-auto inline-flex items-center gap-1.5 text-sm font-semibold text-[#0071e3] hover:text-[#0077ed] transition-colors">
        {{ cta }}
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </NuxtLink>
    </div>

    <!-- Hover overlay -->
    <div class="pointer-events-none absolute inset-0 transform-gpu transition-all duration-300 group-hover:bg-black/[0.02]" />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  name: string
  className?: string
  description: string
  href: string
  cta: string
}>()
</script>
