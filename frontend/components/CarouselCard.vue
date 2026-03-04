<template>
  <div class="card-hover group cursor-pointer" @click="$router.push(`/carousels/${carousel.id}/edit`)">
    <!-- Preview -->
    <div class="slide-aspect relative overflow-hidden bg-[#f5f5f7]">
      <!-- Generating state -->
      <div v-if="carousel.status === 'generating'"
        class="absolute inset-0 flex flex-col items-center justify-center bg-amber-50">
        <div class="w-6 h-6 border-2 border-amber-400 border-t-transparent rounded-full animate-spin mb-2" />
        <span class="text-amber-600 text-xs font-medium">Generating…</span>
      </div>
      <!-- Draft state -->
      <div v-else-if="carousel.status === 'draft'"
        class="absolute inset-0 flex flex-col items-center justify-center gap-2">
        <div class="w-10 h-10 rounded-2xl bg-[#e5e5ea] flex items-center justify-center">
          <svg class="w-5 h-5 text-[#aeaeb2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <span class="text-[#aeaeb2] text-xs">Draft</span>
      </div>
      <!-- Failed state -->
      <div v-else-if="carousel.status === 'failed'"
        class="absolute inset-0 flex flex-col items-center justify-center bg-red-50 gap-1">
        <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span class="text-red-500 text-xs font-medium">Failed</span>
      </div>
      <!-- Ready preview -->
      <div v-else class="absolute inset-0 flex flex-col p-4 overflow-hidden" :style="previewStyle">
        <div class="text-[7px] font-bold leading-tight mb-1 line-clamp-2" :style="{ color: tpl.title }">
          {{ firstSlideTitle || carousel.title }}
        </div>
        <div class="text-[6px] leading-relaxed line-clamp-4 opacity-80" :style="{ color: tpl.body }">
          {{ firstSlideBody || 'Slide content' }}
        </div>
      </div>
      <!-- Hover overlay -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/[0.03] transition-colors duration-200" />
    </div>

    <!-- Info -->
    <div class="p-3.5">
      <div class="flex items-start gap-2 mb-2">
        <h3 class="flex-1 font-medium text-[13px] text-[#1d1d1f] leading-snug line-clamp-2 min-w-0">
          {{ carousel.title }}
        </h3>
        <span class="shrink-0 mt-0.5" :class="`status-${carousel.status}`">
          {{ carousel.status }}
        </span>
      </div>

      <div class="flex items-center gap-2 text-[11px] text-[#aeaeb2] mb-3">
        <span>{{ formatDate(carousel.created_at) }}</span>
        <template v-if="carousel.format?.slides_count">
          <span class="text-[#d2d2d7]">·</span>
          <span>{{ carousel.format.slides_count }} slides</span>
        </template>
        <template v-if="carousel.format?.language">
          <span class="text-[#d2d2d7]">·</span>
          <span class="uppercase font-semibold">{{ carousel.format.language }}</span>
        </template>
      </div>

      <div class="flex gap-1.5" @click.stop>
        <NuxtLink :to="`/carousels/${carousel.id}/edit`"
          class="btn-primary text-xs px-3 py-1.5 flex-1 justify-center">
          {{ carousel.status === 'draft' ? 'Open' : 'Edit' }}
        </NuxtLink>
        <button v-if="carousel.status === 'draft'"
          class="btn-secondary text-xs px-3 py-1.5"
          @click="$emit('generate', carousel.id)">
          Generate
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Carousel } from "~/types"

const props = defineProps<{
  carousel: Carousel
  firstSlideTitle?: string
  firstSlideBody?: string
}>()

defineEmits<{ generate: [id: string] }>()

const TEMPLATES: Record<string, { bg: string; title: string; body: string }> = {
  classic: { bg: "#ffffff", title: "#1a1a1a", body: "#444444" },
  bold:    { bg: "#0f0f0f", title: "#ffffff", body: "#e0e0e0" },
  minimal: { bg: "#f8f8f6", title: "#222222", body: "#555555" },
}

const tpl = computed(() => TEMPLATES[props.carousel.design?.template || "classic"] || TEMPLATES.classic)
const previewStyle = computed(() => ({
  backgroundColor: props.carousel.design?.bg_color || tpl.value.bg,
  fontFamily: "-apple-system, BlinkMacSystemFont, sans-serif",
}))

const formatDate = (d: string) =>
  new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric" })
</script>
