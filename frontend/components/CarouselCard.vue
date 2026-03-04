<template>
  <div class="card-hover group" @click="$router.push(`/carousels/${carousel.id}/edit`)">

    <!-- Slide preview area -->
    <div class="slide-aspect relative overflow-hidden bg-[#f2f2f7]">

      <!-- Generating -->
      <div v-if="carousel.status === 'generating'"
        class="absolute inset-0 flex flex-col items-center justify-center bg-amber-50 gap-2.5">
        <div class="w-7 h-7 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
        <span class="text-amber-900 text-xs font-semibold">Generating…</span>
      </div>

      <!-- Draft -->
      <div v-else-if="carousel.status === 'draft'"
        class="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-[#f2f2f7]">
        <div class="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center ring-1 ring-black/[0.04]">
          <svg class="w-5 h-5 text-[#8e8e93]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <span class="text-[#8e8e93] text-xs font-semibold uppercase tracking-wide">Draft</span>
      </div>

      <!-- Failed -->
      <div v-else-if="carousel.status === 'failed'"
        class="absolute inset-0 flex flex-col items-center justify-center bg-red-50 gap-2.5">
        <div class="w-10 h-10 rounded-xl bg-red-100 flex items-center justify-center">
          <svg class="w-5 h-5 text-red-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <span class="text-red-900 text-xs font-semibold">Generation failed</span>
      </div>

      <!-- Ready: real slide preview -->
      <div v-else class="absolute inset-0">
        <SlidePreview
          :slide="firstSlide"
          :design="carousel.design"
          :slide-number="1"
          :total-slides="carousel.format?.slides_count || 1"
          :small="true"
        />
      </div>

      <!-- Hover shimmer -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/[0.03] transition-colors duration-200" />
    </div>

    <!-- Card body -->
    <div class="p-4">
      <!-- Title + status -->
      <div class="flex items-start gap-2 mb-2">
        <h3 class="flex-1 font-semibold text-[14px] text-[#1c1c1e] leading-snug line-clamp-2 min-w-0">
          {{ carousel.title }}
        </h3>
        <span class="shrink-0 mt-0.5" :class="`status-${carousel.status}`">
          {{ statusLabel }}
        </span>
      </div>

      <!-- Meta row -->
      <div class="flex items-center flex-wrap gap-x-2 gap-y-0.5 text-[12px] text-[#3a3a3c] mb-4">
        <span>{{ formatDate(carousel.created_at) }}</span>
        <template v-if="carousel.format?.language">
          <span class="text-[#c6c6c8]">·</span>
          <span class="font-bold uppercase text-[11px]">{{ carousel.format.language }}</span>
        </template>
        <template v-if="carousel.source_type">
          <span class="text-[#c6c6c8]">·</span>
          <span class="capitalize">{{ carousel.source_type }}</span>
        </template>
      </div>

      <!-- Actions -->
      <div class="flex gap-2" @click.stop>
        <NuxtLink :to="`/carousels/${carousel.id}/edit`"
          class="btn-primary text-[13px] px-3 py-2 flex-1 justify-center">
          {{ carousel.status === 'draft' ? 'Open' : 'Edit' }}
        </NuxtLink>
        <button v-if="carousel.status === 'draft' || carousel.status === 'failed'"
          class="btn-secondary text-[13px] px-3 py-2"
          @click="$emit('generate', carousel.id)">
          Generate
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

defineEmits<{ generate: [id: string] }>()

const statusLabel = computed(() => ({
  draft: "Draft",
  generating: "Generating",
  ready: "Ready",
  failed: "Failed",
}[props.carousel.status] ?? props.carousel.status))

const formatDate = (d: string) =>
  new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
</script>
