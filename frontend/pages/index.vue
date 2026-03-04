<template>
  <div class="min-h-screen bg-[#f2f2f7]">
    <OnboardingModal />
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-black/[0.07]">
      <div class="max-w-6xl mx-auto px-5 sm:px-8 h-14 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-[#0071e3] rounded-[10px] flex items-center justify-center shadow-sm">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </div>
          <span class="font-bold text-[#1c1c1e] tracking-tight text-[15px]">CarouselGen</span>
        </div>
        <NuxtLink to="/carousels/new" class="btn-primary gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
          </svg>
          New Carousel
        </NuxtLink>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-5 sm:px-8 py-10">

      <!-- Empty state -->
      <div v-if="!loading && carousels.length === 0"
        class="flex flex-col items-center justify-center py-28 text-center">
        <div class="w-24 h-24 bg-white rounded-[28px] shadow-[0_4px_32px_rgba(0,0,0,0.10)]
                    flex items-center justify-center mb-8 ring-1 ring-black/[0.04]">
          <svg class="w-11 h-11 text-[#8e8e93]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4"
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h2 class="text-[22px] font-bold text-[#1c1c1e] mb-2 tracking-tight">No carousels yet</h2>
        <p class="text-[#3a3a3c] text-[15px] mb-8 max-w-sm leading-relaxed">
          Turn articles, videos, or links into beautiful Instagram carousels in seconds — powered by AI.
        </p>
        <NuxtLink to="/carousels/new" class="btn-primary px-7 py-2.5 text-[15px]">
          Create your first carousel
        </NuxtLink>
      </div>

      <!-- Loading skeletons -->
      <div v-else-if="loading">
        <div class="flex items-center justify-between mb-7">
          <div class="h-7 w-40 bg-[#e5e5ea] rounded-xl animate-pulse" />
          <div class="h-5 w-16 bg-[#e5e5ea] rounded-lg animate-pulse" />
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="i in 8" :key="i" class="card animate-pulse">
            <div class="slide-aspect bg-[#f2f2f7]" />
            <div class="p-4 space-y-2.5">
              <div class="h-4 bg-[#e5e5ea] rounded-lg w-3/4" />
              <div class="h-3 bg-[#e5e5ea] rounded-lg w-1/2" />
              <div class="h-9 bg-[#e5e5ea] rounded-xl mt-3" />
            </div>
          </div>
        </div>
      </div>

      <!-- Carousels grid -->
      <div v-else>
        <div class="flex items-center justify-between mb-7">
          <div>
            <h1 class="text-[22px] font-bold tracking-tight text-[#1c1c1e]">My Carousels</h1>
            <p class="text-[13px] text-[#3a3a3c] mt-0.5">{{ carousels.length }} carousel{{ carousels.length !== 1 ? 's' : '' }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <CarouselCard
            v-for="carousel in carousels"
            :key="carousel.id"
            :carousel="carousel"
            :first-slide="firstSlides[carousel.id]"
            @generate="handleGenerate"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import type { Carousel, Slide } from "~/types"

const { fetchCarousels } = useCarousels()
const { startGeneration, pollGeneration } = useGeneration()
const config = useRuntimeConfig()

const loading = ref(true)
const carousels = ref<Carousel[]>([])
const firstSlides = ref<Record<string, Slide>>({})

const load = async () => {
  try {
    const data = await fetchCarousels()
    carousels.value = data
    await Promise.all(
      data.filter((x) => x.status === "ready").map(async (c) => {
        try {
          const slides = await $fetch<any[]>(`${config.public.apiBase}/carousels/${c.id}/slides`)
          if (slides.length > 0) firstSlides.value[c.id] = slides[0]
        } catch {}
      })
    )
  } finally {
    loading.value = false
  }
}

const handleGenerate = async (carouselId: string) => {
  const c = carousels.value.find((x) => x.id === carouselId)
  if (!c) return
  c.status = "generating"
  try {
    const gen = await startGeneration(carouselId)
    pollGeneration(
      gen.id,
      async () => {
        const updated = await $fetch<Carousel>(`${config.public.apiBase}/carousels/${carouselId}`)
        const idx = carousels.value.findIndex((x) => x.id === carouselId)
        if (idx !== -1) carousels.value[idx] = updated
      },
      () => {
        const c2 = carousels.value.find((x) => x.id === carouselId)
        if (c2) c2.status = "failed"
      },
    )
  } catch {
    if (c) c.status = "failed"
  }
}

let pollInterval: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  await load()
  pollInterval = setInterval(async () => {
    if (carousels.value.some((c) => c.status === "generating")) {
      const data = await fetchCarousels()
      carousels.value = data
    }
  }, 5000)
})

onUnmounted(() => { if (pollInterval) clearInterval(pollInterval) })
</script>
