<template>
  <div class="h-screen bg-[#f5f5f7] flex flex-col overflow-hidden">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-[#fbfbfd]/90 backdrop-blur-xl border-b border-black/[0.06] shrink-0">
      <div class="px-4 h-14 flex items-center gap-3">
        <NuxtLink to="/"
          class="w-8 h-8 rounded-xl flex items-center justify-center text-[#6e6e73] hover:bg-black/5 transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </NuxtLink>

        <div class="flex-1 min-w-0">
          <input
            v-if="carousel"
            v-model="editableTitle"
            class="font-semibold text-[#1d1d1f] text-sm bg-transparent border-0 focus:outline-none focus:ring-0 w-full truncate placeholder:text-[#aeaeb2]"
            placeholder="Untitled carousel"
            @blur="saveTitle"
          />
          <div v-else class="h-4 bg-[#e5e5ea] rounded-lg animate-pulse w-40" />
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <span v-if="carousel" :class="`tag tag-${carousel.status}`">
            {{ carousel.status }}
          </span>

          <button
            v-if="carousel && (carousel.status === 'ready' || carousel.status === 'failed')"
            class="btn-secondary text-xs px-3 py-1.5 gap-1.5"
            :disabled="generating"
            @click="handleRegenerate"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Regenerate
          </button>

          <button
            v-if="carousel?.status === 'ready'"
            class="btn-primary text-xs px-3 py-1.5 gap-1.5"
            :disabled="exporting"
            @click="handleExport"
          >
            <svg v-if="exporting" class="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ exporting ? exportStatus : 'Export ZIP' }}
          </button>
        </div>
      </div>
    </header>

    <!-- Generation banner -->
    <div
      v-if="generating || carousel?.status === 'generating'"
      class="shrink-0 bg-amber-50/90 backdrop-blur-sm border-b border-amber-200/60 px-5 py-2.5 flex items-center gap-3"
    >
      <div class="w-4 h-4 border-2 border-amber-500 border-t-transparent rounded-full animate-spin shrink-0" />
      <span class="text-sm text-amber-700 font-medium">Generating slides with AI…</span>
    </div>

    <!-- Main layout -->
    <div v-if="carousel" class="flex flex-1 overflow-hidden">
      <div class="flex flex-col lg:flex-row w-full flex-1 overflow-hidden">

        <!-- Slide list sidebar -->
        <div class="lg:w-24 shrink-0 bg-[#fbfbfd] border-b lg:border-b-0 lg:border-r border-black/[0.06] overflow-x-auto lg:overflow-y-auto lg:overflow-x-hidden">
          <div class="flex lg:flex-col gap-2 p-2.5">
            <button
              v-for="(slide, i) in slides"
              :key="slide.id"
              class="relative shrink-0 w-16 lg:w-full rounded-xl overflow-hidden border-2 transition-all duration-150"
              :class="activeIndex === i
                ? 'border-[#0071e3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
                : 'border-transparent hover:border-[#d2d2d7]'"
              @click="activeIndex = i"
            >
              <SlidePreview :slide="slide" :design="design" :small="true" />
              <div class="absolute bottom-1 left-1 bg-black/40 backdrop-blur-sm text-white text-[9px] font-semibold rounded-md px-1 leading-tight">
                {{ i + 1 }}
              </div>
            </button>

            <div v-if="slides.length === 0 && !generating"
              class="flex flex-col items-center justify-center py-6 text-[#aeaeb2] text-[10px] text-center gap-1 lg:w-full">
              <svg class="w-5 h-5 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              No slides
            </div>
          </div>
        </div>

        <!-- Center: preview + editor -->
        <div class="flex-1 flex flex-col lg:flex-row overflow-hidden">
          <div class="flex-1 p-4 lg:p-8 flex items-start lg:items-center justify-center overflow-y-auto">

            <!-- Generating placeholder -->
            <div v-if="generating || carousel.status === 'generating'" class="text-center">
              <div class="w-14 h-14 border-[3px] border-[#0071e3]/20 border-t-[#0071e3] rounded-full animate-spin mx-auto mb-5" />
              <p class="text-[#6e6e73] font-medium">Generating your slides…</p>
              <p class="text-[#aeaeb2] text-sm mt-1">This takes about 15–30 seconds</p>
            </div>

            <!-- Empty state -->
            <div v-else-if="slides.length === 0" class="text-center">
              <div class="w-16 h-16 bg-white rounded-3xl shadow-[0_4px_24px_rgba(0,0,0,0.08)] flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-[#aeaeb2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <p class="text-[#6e6e73] font-medium mb-1">No slides yet</p>
              <p class="text-[#aeaeb2] text-sm">Generate slides to get started</p>
            </div>

            <!-- Slide content -->
            <div v-else class="w-full max-w-xs">
              <SlidePreview
                :slide="activeSlide"
                :design="design"
                :slide-number="activeIndex + 1"
                :total-slides="slides.length"
                :show-counter="true"
              />

              <!-- Text editor card -->
              <div class="mt-4 card p-5 space-y-4">
                <div>
                  <label class="label">Title</label>
                  <input v-model="editTitle" class="input" placeholder="Slide title" @blur="saveSlide" />
                </div>
                <div>
                  <label class="label">Body</label>
                  <textarea v-model="editBody" class="input min-h-[90px] resize-none leading-relaxed"
                    placeholder="Slide body text" @blur="saveSlide" />
                </div>
                <div>
                  <label class="label">
                    CTA
                    <span class="text-[#aeaeb2] normal-case font-normal tracking-normal ml-1">— optional</span>
                  </label>
                  <input v-model="editCta" class="input" placeholder="e.g., Save this post ↓" @blur="saveSlide" />
                </div>
                <div v-if="savingSlide" class="text-[11px] text-[#aeaeb2] text-right">Saving…</div>
              </div>

              <!-- Navigation -->
              <div class="flex items-center justify-between mt-3">
                <button class="btn-secondary text-sm px-3 py-1.5 gap-1.5"
                  :disabled="activeIndex === 0"
                  @click="activeIndex--">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                  Prev
                </button>
                <span class="text-sm text-[#6e6e73] font-medium tabular-nums">{{ activeIndex + 1 }} / {{ slides.length }}</span>
                <button class="btn-secondary text-sm px-3 py-1.5 gap-1.5"
                  :disabled="activeIndex === slides.length - 1"
                  @click="activeIndex++">
                  Next
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Design panel -->
          <div class="lg:w-72 shrink-0 bg-white border-t lg:border-t-0 lg:border-l border-black/[0.06] flex flex-col overflow-hidden">
            <DesignPanel
              v-model="design"
              :saving="savingDesign"
              @save="saveDesign"
              @apply-to-all="saveDesign"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-else class="flex-1 flex items-center justify-center">
      <div class="w-10 h-10 border-[3px] border-[#0071e3]/20 border-t-[#0071e3] rounded-full animate-spin" />
    </div>

    <!-- Export success toast -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="translate-y-4 opacity-0 scale-95"
        enter-to-class="translate-y-0 opacity-100 scale-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="translate-y-0 opacity-100 scale-100"
        leave-to-class="translate-y-4 opacity-0 scale-95"
      >
        <div
          v-if="exportUrl"
          class="fixed bottom-6 right-6 bg-white/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_40px_rgba(0,0,0,0.15)] border border-white/50 p-4 flex items-center gap-3 z-50 max-w-sm"
        >
          <div class="w-9 h-9 bg-[#34c759]/10 rounded-xl flex items-center justify-center shrink-0">
            <svg class="w-4 h-4 text-[#34c759]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-[#1d1d1f]">Export ready!</p>
            <p class="text-xs text-[#6e6e73] mt-0.5">Your ZIP is ready to download</p>
          </div>
          <a :href="exportUrl" download class="btn-primary text-xs px-3 py-1.5">Download</a>
          <button class="w-6 h-6 flex items-center justify-center rounded-full text-[#aeaeb2] hover:text-[#6e6e73] hover:bg-black/5 transition-colors text-lg leading-none"
            @click="exportUrl = null">×</button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import type { Carousel, Slide, CarouselDesign } from "~/types"
import { DEFAULT_DESIGN } from "~/types"

const route = useRoute()
const config = useRuntimeConfig()
const { fetchCarousel, updateCarousel, updateDesign } = useCarousels()
const { startGeneration, pollGeneration } = useGeneration()
const { startExport, pollExport } = useExport()

const carouselId = route.params.id as string
const genIdFromQuery = route.query.gen as string | undefined

const carousel = ref<Carousel | null>(null)
const slides = ref<Slide[]>([])
const activeIndex = ref(0)
const editableTitle = ref("")
const generating = ref(false)
const savingSlide = ref(false)
const savingDesign = ref(false)
const exporting = ref(false)
const exportStatus = ref("Exporting…")
const exportUrl = ref<string | null>(null)
const design = ref<CarouselDesign>({ ...DEFAULT_DESIGN })

const editTitle = ref("")
const editBody = ref("")
const editCta = ref("")

const activeSlide = computed(() => slides.value[activeIndex.value] ?? null)

watch(activeSlide, (s) => {
  if (s) {
    editTitle.value = s.title
    editBody.value = s.body
    editCta.value = s.footer_cta || ""
  }
})

const loadData = async () => {
  const [c, sl] = await Promise.all([
    fetchCarousel(carouselId),
    $fetch<Slide[]>(`${config.public.apiBase}/carousels/${carouselId}/slides`),
  ])
  carousel.value = c
  slides.value = sl
  editableTitle.value = c.title
  design.value = { ...DEFAULT_DESIGN, ...c.design }
  if (sl.length > 0) {
    editTitle.value = sl[0].title
    editBody.value = sl[0].body
    editCta.value = sl[0].footer_cta || ""
  }
}

const saveTitle = async () => {
  if (!carousel.value || editableTitle.value === carousel.value.title) return
  await updateCarousel(carouselId, { title: editableTitle.value })
}

const saveSlide = async () => {
  const slide = activeSlide.value
  if (!slide) return
  savingSlide.value = true
  try {
    const updated = await $fetch<Slide>(`${config.public.apiBase}/carousels/${carouselId}/slides/${slide.id}`, {
      method: "PATCH",
      body: { title: editTitle.value, body: editBody.value, footer_cta: editCta.value || null },
    })
    slides.value[activeIndex.value] = updated
  } finally {
    savingSlide.value = false
  }
}

const saveDesign = async (d: CarouselDesign) => {
  savingDesign.value = true
  try {
    const updated = await updateDesign(carouselId, d)
    carousel.value = updated
    design.value = { ...DEFAULT_DESIGN, ...updated.design }
  } finally {
    savingDesign.value = false
  }
}

const startPollGeneration = (genId: string) => {
  generating.value = true
  if (carousel.value) carousel.value.status = "generating"
  pollGeneration(
    genId,
    async () => {
      generating.value = false
      await loadData()
    },
    () => {
      generating.value = false
      if (carousel.value) carousel.value.status = "failed"
    },
  )
}

const handleRegenerate = async () => {
  const gen = await startGeneration(carouselId)
  startPollGeneration(gen.id)
}

const handleExport = async () => {
  exporting.value = true
  exportStatus.value = "Queuing…"
  try {
    const exp = await startExport(carouselId)
    exportStatus.value = "Rendering…"
    pollExport(
      exp.id,
      (done) => {
        exporting.value = false
        if (done.file_url) exportUrl.value = done.file_url
      },
      () => {
        exporting.value = false
        alert("Export failed. Please try again.")
      },
    )
  } catch {
    exporting.value = false
    alert("Export failed.")
  }
}

onMounted(async () => {
  await loadData()
  if (genIdFromQuery) {
    startPollGeneration(genIdFromQuery)
  }
})
</script>
