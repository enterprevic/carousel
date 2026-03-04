<template>
  <div class="min-h-screen bg-[#f5f5f7]">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-[#fbfbfd]/90 backdrop-blur-xl border-b border-black/[0.06]">
      <div class="max-w-6xl mx-auto px-5 sm:px-8 h-14 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 bg-[#0071e3] rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </div>
          <span class="font-semibold text-[#1d1d1f] tracking-tight">CarouselGen</span>
        </div>
        <NuxtLink to="/carousels/new" class="btn-primary text-sm">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
          </svg>
          New Carousel
        </NuxtLink>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-5 sm:px-8 py-10">
      <!-- Empty state -->
      <div v-if="!loading && carousels.length === 0" class="flex flex-col items-center justify-center py-32 text-center">
        <div class="w-20 h-20 bg-white rounded-3xl shadow-[0_4px_24px_rgba(0,0,0,0.08)] flex items-center justify-center mb-6">
          <svg class="w-9 h-9 text-[#aeaeb2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-[#1d1d1f] mb-2">No carousels yet</h2>
        <p class="text-[#6e6e73] text-sm mb-8 max-w-xs leading-relaxed">
          Create beautiful Instagram carousels from text or video in seconds with AI
        </p>
        <NuxtLink to="/carousels/new" class="btn-primary px-6 py-2.5 text-sm">
          Create your first carousel
        </NuxtLink>
      </div>

      <!-- Loading skeletons -->
      <div v-else-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="i in 8" :key="i" class="card animate-pulse">
          <div class="slide-aspect bg-[#f5f5f7]" />
          <div class="p-4 space-y-2">
            <div class="h-3.5 bg-[#e5e5ea] rounded-lg w-3/4" />
            <div class="h-3 bg-[#e5e5ea] rounded-lg w-1/2" />
            <div class="h-8 bg-[#e5e5ea] rounded-xl mt-3" />
          </div>
        </div>
      </div>

      <!-- Carousels grid -->
      <div v-else>
        <div class="flex items-center justify-between mb-7">
          <h1 class="text-2xl font-bold tracking-tight text-[#1d1d1f]">My Carousels</h1>
          <span class="text-sm text-[#aeaeb2]">{{ carousels.length }} total</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <CarouselCard
            v-for="carousel in carousels"
            :key="carousel.id"
            :carousel="carousel"
            :first-slide-title="firstSlideTitles[carousel.id]"
            :first-slide-body="firstSlideBodies[carousel.id]"
            @generate="handleGenerate"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import type { Carousel } from "~/types"

const { fetchCarousels } = useCarousels()
const { startGeneration, pollGeneration } = useGeneration()
const config = useRuntimeConfig()

const loading = ref(true)
const carousels = ref<Carousel[]>([])
const firstSlideTitles = ref<Record<string, string>>({})
const firstSlideBodies = ref<Record<string, string>>({})

const load = async () => {
  try {
    const data = await fetchCarousels()
    carousels.value = data
    for (const c of data.filter((x) => x.status === "ready")) {
      try {
        const slides = await $fetch<any[]>(`${config.public.apiBase}/carousels/${c.id}/slides`)
        if (slides.length > 0) {
          firstSlideTitles.value[c.id] = slides[0].title
          firstSlideBodies.value[c.id] = slides[0].body
        }
      } catch {}
    }
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
