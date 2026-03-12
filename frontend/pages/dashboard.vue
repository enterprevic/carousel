<template>
  <div class="flex-1 overflow-y-auto flex flex-col min-h-0">
    <OnboardingModal />
    <ToastContainer />

    <!-- Main content area -->
    <div class="flex-1 m-4 bg-white rounded-[20px] flex flex-col overflow-hidden">

      <!-- Header bar -->
      <div class="px-6 pt-6 pb-0 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
          <h1 class="text-[24px] font-semibold text-[#000000] leading-[29px]">{{ t.navCarousels }}</h1>
        </div>

        <div class="flex items-center gap-4">
          <!-- My Context button -->
          <button class="flex items-center gap-2 bg-[#F4F5F6] rounded-[16px] px-3 py-3 text-[#171C1F] text-[15px] font-semibold leading-[24px] tracking-[0.3px] transition-colors hover:bg-[#E6E8EA]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span class="px-1">{{ t.navMyContext }}</span>
          </button>

          <!-- Create button -->
          <NuxtLink to="/carousels/new"
            class="flex items-center gap-2 bg-[#2B31B3] rounded-[16px] px-4 py-3 text-white text-[15px] font-semibold leading-[24px] tracking-[0.3px] transition-colors hover:bg-[#2228a0]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span class="px-1">{{ t.navCreate }}</span>
          </NuxtLink>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex-1 px-6 pt-6">
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="i in 8" :key="i" class="bg-[#F4F5F6] rounded-2xl animate-pulse">
            <div class="slide-aspect" />
            <div class="p-4 space-y-2.5">
              <div class="h-4 bg-[#E6E8EA] rounded-lg w-3/4" />
              <div class="h-3 bg-[#E6E8EA] rounded-lg w-1/2" />
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="carousels.length === 0"
        class="flex-1 flex flex-col items-center justify-center px-6 gap-8">

        <!-- 3 tilted card mockups -->
        <div class="flex items-center justify-center gap-2 select-none">
          <!-- Left card (rotated -8deg) -->
          <div class="w-[95px] h-[130px] rounded-[12px] bg-[#E6E8EA] overflow-hidden flex flex-col gap-[7px] p-[12px]"
            style="transform: rotate(-8deg); transform-origin: center;">
            <div class="flex flex-col gap-1">
              <div class="w-full h-[15px] rounded-[6px] bg-[#A0ADB4]" />
              <div class="w-[55%] h-[14px] rounded-[6px] bg-[#A0ADB4]" />
            </div>
            <div class="w-full h-[6px] rounded-full bg-[#A0ADB4]" />
            <div class="w-full h-[6px] rounded-full bg-[#A0ADB4]" />
            <div class="w-full h-[6px] rounded-full bg-[#A0ADB4]" />
          </div>

          <!-- Center card (no rotation, larger) -->
          <div class="w-[124px] h-[170px] rounded-[16px] bg-[#E6E8EA] overflow-hidden flex flex-col gap-[10px] p-[16px]">
            <div class="w-[78px] h-[19px] rounded-[8px] bg-[#A0ADB4]" />
            <div class="w-full h-[8px] rounded-full bg-[#A0ADB4]" />
            <div class="w-full h-[8px] rounded-full bg-[#A0ADB4]" />
            <div class="w-full h-[8px] rounded-full bg-[#A0ADB4]" />
          </div>

          <!-- Right card (rotated +8deg) -->
          <div class="w-[95px] h-[130px] rounded-[12px] bg-[#E6E8EA] overflow-hidden flex flex-col gap-[7px] p-[12px]"
            style="transform: rotate(8deg); transform-origin: center;">
            <div class="flex flex-col gap-1">
              <div class="w-[60px] h-[14px] rounded-[6px] bg-[#A0ADB4]" />
              <div class="w-full h-[14px] rounded-[6px] bg-[#A0ADB4]" />
            </div>
            <div class="w-full h-[6px] rounded-full bg-[#A0ADB4]" />
            <div class="w-full h-[6px] rounded-full bg-[#A0ADB4]" />
            <div class="w-full h-[6px] rounded-full bg-[#A0ADB4]" />
          </div>
        </div>

        <!-- Text + CTA -->
        <div class="flex flex-col items-center gap-6 max-w-[600px] text-center">
          <div class="flex flex-col gap-3">
            <h2 class="text-[20px] font-semibold text-[#000000] leading-[24px] tracking-[0.15px]">
              {{ t.dashCreateTitle }}
            </h2>
            <p class="text-[16px] text-[#4E616B] leading-[24px] tracking-[0.5px]">
              {{ t.dashCreateDesc }}
            </p>
          </div>

          <NuxtLink to="/carousels/new"
            class="flex items-center gap-2 bg-[#2B31B3] rounded-[16px] px-6 py-4 text-white text-[17px] font-semibold leading-[24px] tracking-[0.25px] transition-colors hover:bg-[#2228a0]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>{{ t.dashAdd }}</span>
          </NuxtLink>
        </div>
      </div>

      <!-- Carousels grid -->
      <div v-else class="flex-1 overflow-y-auto px-6 pt-6 pb-6">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-2 text-xs flex-wrap">
            <span class="px-2.5 py-1 rounded-full bg-[#F4F5F6] border border-[#E6E8EA] text-[#3a3a3c] font-medium">
              {{ stats.total }} {{ t.dashTotal }}
            </span>
            <span v-if="stats.ready > 0" class="px-2.5 py-1 rounded-full bg-[#34c759]/10 text-[#1a7f37] font-medium">
              {{ stats.ready }} {{ t.dashReady }}
            </span>
            <span v-if="stats.draft > 0" class="px-2.5 py-1 rounded-full bg-[#F4F5F6] text-[#8e8e93] font-medium">
              {{ stats.draft }} {{ t.dashDraft }}
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

    </div>
  </div>
</template>

<script setup lang="ts">
import type { Carousel, Slide } from "~/types"

definePageMeta({ layout: 'default', ssr: false })

const { fetchCarousels, deleteCarousel } = useCarousels()
const { t } = useLang()
const { startGeneration, pollGeneration } = useGeneration()
const { authHeaders } = useAuth()
const { show: showToast } = useToast()
const config = useRuntimeConfig()

const loading = ref(true)
const carousels = ref<Carousel[]>([])
const firstSlides = ref<Record<string, Slide>>({})

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
