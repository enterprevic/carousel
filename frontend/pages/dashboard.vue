<template>
  <div class="min-h-screen bg-[#f2f2f7]">
    <OnboardingModal />
    <ToastContainer />
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/90 backdrop-blur-xl border-b border-black/[0.06]">
      <div class="max-w-6xl mx-auto px-5 sm:px-8 h-15 flex items-center justify-between" style="height:60px">
        <!-- Logo -->
        <NuxtLink to="/dashboard" class="flex items-center gap-2.5 select-none">
          <div class="w-9 h-9 rounded-[11px] flex items-center justify-center shadow-[0_2px_8px_rgba(0,113,227,0.30)] shrink-0 overflow-hidden" style="background:#0071e3">
            <svg viewBox="0 0 36 36" width="36" height="36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- top-left: fully opaque -->
              <rect x="6" y="6" width="10" height="10" rx="3" fill="white"/>
              <!-- top-right: slightly faded -->
              <rect x="20" y="6" width="10" height="10" rx="3" fill="white" fill-opacity="0.6"/>
              <!-- bottom-left: slightly faded -->
              <rect x="6" y="20" width="10" height="10" rx="3" fill="white" fill-opacity="0.6"/>
              <!-- bottom-right: most faded — depth cue -->
              <rect x="20" y="20" width="10" height="10" rx="3" fill="white" fill-opacity="0.3"/>
            </svg>
          </div>
          <div class="flex flex-col leading-none">
            <span class="font-bold text-[#1c1c1e] text-[15px] tracking-tight">CarouselGen</span>
            <span class="text-[10px] text-[#8e8e93] font-medium tracking-wide mt-0.5">AI Carousel Studio</span>
          </div>
        </NuxtLink>

        <!-- Right side -->
        <div class="flex items-center gap-2.5">
          <NuxtLink to="/carousels/new"
            class="btn-primary gap-1.5 text-[13px] px-3.5 py-2"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
            </svg>
            New
          </NuxtLink>

          <!-- Avatar -->
          <NuxtLink to="/profile"
            class="flex items-center gap-2 pl-1 pr-2.5 py-1 rounded-2xl hover:bg-black/[0.04] transition-colors group select-none"
            :title="username ? username : 'Profile'"
          >
            <div class="w-7 h-7 rounded-xl bg-[#0071e3] flex items-center justify-center text-white text-[12px] font-bold shadow-sm shrink-0">
              {{ initial }}
            </div>
            <span v-if="username" class="text-[13px] font-medium text-[#3a3a3c] group-hover:text-[#1c1c1e] transition-colors hidden sm:block">
              {{ username }}
            </span>
          </NuxtLink>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-5 sm:px-8 py-10">

      <!-- Empty state / getting started -->
      <div v-if="!loading && carousels.length === 0" class="max-w-xl mx-auto py-16">
        <div class="text-center mb-10">
          <h2 class="text-[22px] font-bold text-[#1c1c1e] mb-2 tracking-tight">Create your first carousel</h2>
          <p class="text-[#3a3a3c] text-[15px] leading-relaxed">
            Paste content, let AI generate slides, then style and export.
          </p>
        </div>

        <!-- Steps -->
        <div class="space-y-3 mb-10">
          <div v-for="(step, i) in gettingStartedSteps" :key="i"
            class="card flex items-center gap-4 px-5 py-4">
            <div class="w-8 h-8 rounded-xl bg-[#0071e3]/10 flex items-center justify-center shrink-0">
              <svg class="w-4 h-4 text-[#0071e3]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="step.icon" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-[#1c1c1e]">{{ step.title }}</p>
              <p class="text-xs text-[#8e8e93] mt-0.5">{{ step.desc }}</p>
            </div>
            <div class="w-6 h-6 rounded-full bg-[#f2f2f7] flex items-center justify-center shrink-0 text-xs font-bold text-[#8e8e93]">
              {{ i + 1 }}
            </div>
          </div>
        </div>

        <NuxtLink to="/carousels/new" class="btn-primary w-full py-3 text-[15px] justify-center">
          Get started
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
        <div class="flex items-center justify-between mb-6">
          <div>
            <h1 class="text-[22px] font-bold tracking-tight text-[#1c1c1e]">My Carousels</h1>
          </div>
          <!-- Stats pills -->
          <div class="flex items-center gap-1.5 sm:gap-2 text-xs flex-wrap justify-end">
            <span class="px-2 sm:px-2.5 py-1 rounded-full bg-white border border-[#e5e5ea] text-[#3a3a3c] font-medium whitespace-nowrap">
              {{ stats.total }} total
            </span>
            <span v-if="stats.ready > 0" class="px-2 sm:px-2.5 py-1 rounded-full bg-[#34c759]/10 text-[#1a7f37] font-medium whitespace-nowrap">
              {{ stats.ready }} ready
            </span>
            <span v-if="stats.draft > 0" class="px-2 sm:px-2.5 py-1 rounded-full bg-[#f2f2f7] text-[#8e8e93] font-medium whitespace-nowrap">
              {{ stats.draft }} draft
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <CarouselCard
            v-for="carousel in carousels"
            :key="carousel.id"
            :carousel="carousel"
            :first-slide="firstSlides[carousel.id]"
            @generate="handleGenerate"
            @delete="handleDelete"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import type { Carousel, Slide } from "~/types"

const { fetchCarousels, deleteCarousel } = useCarousels()
const { startGeneration, pollGeneration } = useGeneration()
const { authHeaders, logout, getUsername } = useAuth()
const { show: showToast } = useToast()
const config = useRuntimeConfig()

const username = import.meta.client ? getUsername() : ''
const initial = computed(() => username?.[0]?.toUpperCase() ?? '?')

const loading = ref(true)
const carousels = ref<Carousel[]>([])
const firstSlides = ref<Record<string, Slide>>({})

const gettingStartedSteps = [
  { title: "Add your content", desc: "Paste text, a video URL, or a list of links.", icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" },
  { title: "Generate slides with AI", desc: "Choose slide count, language, and style.", icon: "M13 10V3L4 14h7v7l9-11h-7z" },
  { title: "Design each slide", desc: "Edit text, pick templates, upload backgrounds.", icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" },
  { title: "Export as ZIP", desc: "Download 1080×1350 px PNGs ready for Instagram.", icon: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" },
]

const stats = computed(() => ({
  total: carousels.value.length,
  ready: carousels.value.filter((c) => c.status === 'ready').length,
  draft: carousels.value.filter((c) => c.status === 'draft').length,
}))

const load = async () => {
  try {
    const data = await fetchCarousels()
    carousels.value = data
    await Promise.all(
      data.filter((x) => x.status === "ready").map(async (c) => {
        try {
          const slides = await $fetch<any[]>(`${config.public.apiBase}/carousels/${c.id}/slides`, { headers: authHeaders() })
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
        const updated = await $fetch<Carousel>(`${config.public.apiBase}/carousels/${carouselId}`, { headers: authHeaders() })
        const idx = carousels.value.findIndex((x) => x.id === carouselId)
        if (idx !== -1) carousels.value[idx] = updated
      },
      () => {
        const c2 = carousels.value.find((x) => x.id === carouselId)
        if (c2) c2.status = "failed"
      },
    )
  } catch (e: any) {
    if (e?.response?.status === 429 || e?.statusCode === 429) {
      if (c) c.status = "draft"
      const detail = e?.data?.detail ?? e?.response?._data?.detail ?? ""
      const match = detail.match(/(\d+)/)
      const wait = match ? ` Please wait ${match[1]}s.` : ""
      showToast(`Slow down!${wait} Generation is limited to once every 30s.`, "warning")
    } else {
      if (c) c.status = "failed"
    }
  }
}

const handleDelete = async (carouselId: string) => {
  try {
    await deleteCarousel(carouselId)
    carousels.value = carousels.value.filter((c) => c.id !== carouselId)
    delete firstSlides.value[carouselId]
  } catch {
    alert("Failed to delete carousel. Please try again.")
  }
}

// Poll only carousels that were already generating when the page loaded.
// Carousels where generation is triggered from this page use SSE via handleGenerate.
let pollInterval: ReturnType<typeof setInterval> | null = null

const pollStaleGenerating = async () => {
  const generating = carousels.value.filter((c) => c.status === "generating")
  if (generating.length === 0) {
    if (pollInterval) { clearInterval(pollInterval); pollInterval = null }
    return
  }
  await Promise.all(generating.map(async (c) => {
    try {
      const updated = await $fetch<Carousel>(`${config.public.apiBase}/carousels/${c.id}`, { headers: authHeaders() })
      const idx = carousels.value.findIndex((x) => x.id === c.id)
      if (idx !== -1 && updated.status !== "generating") carousels.value[idx] = updated
    } catch {}
  }))
}

onMounted(async () => {
  await load()
  if (carousels.value.some((c) => c.status === "generating")) {
    pollInterval = setInterval(pollStaleGenerating, 4000)
  }
})

onUnmounted(() => { if (pollInterval) clearInterval(pollInterval) })
</script>
