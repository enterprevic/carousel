<template>
  <div
    class="group relative flex flex-col overflow-hidden rounded-2xl bg-white border border-black/[0.06] shadow-[0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)] cursor-pointer transition-all duration-300 hover:shadow-[0_0_0_1px_rgba(0,0,0,.06),0_8px_24px_rgba(0,0,0,.09),0_24px_48px_rgba(0,0,0,.10)] hover:-translate-y-0.5"
    @click="$router.push(`/carousels/${carousel.id}/edit`)"
  >
    <!-- Slide preview -->
    <div class="slide-aspect relative overflow-hidden bg-[#f2f2f7] shrink-0">

      <!-- Generating -->
      <div
        v-if="carousel.status === 'generating'"
        class="absolute inset-0 flex flex-col items-center justify-center gap-3"
        style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)"
      >
        <div class="w-10 h-10 rounded-2xl bg-amber-100 flex items-center justify-center">
          <div class="w-5 h-5 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
        <div class="text-center">
          <p class="text-amber-900 text-[11px] font-bold uppercase tracking-widest">Generating</p>
          <p class="text-amber-700 text-[10px] mt-0.5">AI is writing your slides…</p>
        </div>
      </div>

      <!-- Draft -->
      <div
        v-else-if="carousel.status === 'draft'"
        class="absolute inset-0 flex flex-col items-center justify-center gap-3"
        style="background: linear-gradient(135deg, #f5f5f7 0%, #e5e5ea 100%)"
      >
        <div class="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center ring-1 ring-black/[0.06]">
          <svg class="w-5 h-5 text-[#6e6e73]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div class="text-center">
          <p class="text-[#3a3a3c] text-[11px] font-bold uppercase tracking-widest">Draft</p>
          <p class="text-[#8e8e93] text-[10px] mt-0.5">Ready to generate</p>
        </div>
      </div>

      <!-- Failed -->
      <div
        v-else-if="carousel.status === 'failed'"
        class="absolute inset-0 flex flex-col items-center justify-center gap-3"
        style="background: linear-gradient(135deg, #fff5f5 0%, #fee2e2 100%)"
      >
        <div class="w-12 h-12 rounded-2xl bg-red-100 flex items-center justify-center">
          <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div class="text-center">
          <p class="text-red-900 text-[11px] font-bold uppercase tracking-widest">Failed</p>
          <p class="text-red-600 text-[10px] mt-0.5">Tap Generate to retry</p>
        </div>
      </div>

      <!-- Ready: real slide preview -->
      <div v-else class="absolute inset-0">
        <SlidePreview
          :slide="firstSlide"
          :design="carousel.design"
          :slide-number="1"
          :total-slides="carousel.format?.slides_count || 1"
        />
      </div>

      <!-- Slide count chip (bottom-left, ready only) -->
      <div
        v-if="carousel.status === 'ready' && carousel.format?.slides_count"
        class="absolute bottom-2 left-2 pointer-events-none"
      >
        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-black/40 backdrop-blur-sm text-white text-[10px] font-semibold">
          <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
              d="M19 11H5m14 0l-4-4m4 4l-4 4" />
          </svg>
          {{ carousel.format.slides_count }} slides
        </span>
      </div>

      <!-- Hover shimmer -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/[0.03] transition-colors duration-300 pointer-events-none" />
    </div>

    <!-- Info section -->
    <div class="flex flex-col flex-1 p-4 pb-3">
      <!-- Title -->
      <h3 class="font-semibold text-[13.5px] text-[#1c1c1e] leading-snug line-clamp-2 mb-2 transition-transform duration-300 group-hover:-translate-y-0.5">
        {{ carousel.title }}
      </h3>

      <!-- Meta + status row -->
      <div class="flex items-center gap-1.5 text-[11px] text-[#8e8e93] mb-3">
        <span :class="`status-${carousel.status}`" class="!text-[9px] !py-0.5">{{ statusLabel }}</span>
        <span class="text-[#c6c6c8]">·</span>
        <span>{{ formatDate(carousel.created_at) }}</span>
        <template v-if="carousel.format?.language">
          <span class="text-[#c6c6c8]">·</span>
          <span class="font-bold uppercase text-[10px]">{{ carousel.format.language }}</span>
        </template>
      </div>

      <!-- Actions (always visible, CTA slides up on hover) -->
      <div class="flex gap-1 transition-transform duration-300 group-hover:-translate-y-0.5" @click.stop>
        <NuxtLink
          :to="`/carousels/${carousel.id}/edit`"
          class="btn-primary text-[11px] px-2.5 py-1.5 flex-1 justify-center min-w-0"
        >
          {{ carousel.status === 'draft' ? 'Open' : 'Edit' }}
        </NuxtLink>
        <button
          v-if="carousel.status === 'draft' || carousel.status === 'failed'"
          class="btn-secondary text-[11px] px-2.5 py-1.5 shrink-0"
          @click="$emit('generate', carousel.id)"
        >
          Gen
        </button>
        <button
          class="w-7 h-7 flex items-center justify-center rounded-xl text-[#aeaeb2] hover:bg-red-50 hover:text-[#ff3b30] transition-colors shrink-0"
          aria-label="Delete carousel"
          title="Delete carousel"
          @click="handleDelete"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Carousel, Slide } from "~/types"

const props = defineProps<{
  carousel: Carousel
  firstSlide?: Slide | null
}>()

const emit = defineEmits<{ generate: [id: string]; delete: [id: string] }>()

const handleDelete = (e: Event) => {
  e.stopPropagation()
  if (confirm(`Delete "${props.carousel.title}"? This cannot be undone.`)) {
    emit('delete', props.carousel.id)
  }
}

const statusLabel = computed(() => ({
  draft: "Draft",
  generating: "Generating",
  ready: "Ready",
  failed: "Failed",
}[props.carousel.status] ?? props.carousel.status))

const formatDate = (d: string) =>
  new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
</script>
