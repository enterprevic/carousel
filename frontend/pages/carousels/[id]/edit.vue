<template>
  <div class="h-screen bg-[#f2f2f7] flex flex-col overflow-hidden">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-[#fbfbfd]/90 backdrop-blur-xl border-b border-black/[0.06] shrink-0">
      <div class="px-4 h-14 flex items-center gap-3">
        <NuxtLink to="/"
          class="w-8 h-8 rounded-xl flex items-center justify-center text-[#3a3a3c] hover:bg-black/5 transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </NuxtLink>

        <div class="flex-1 min-w-0">
          <input v-if="carousel" v-model="editableTitle"
            class="font-semibold text-[#1c1c1e] text-sm bg-transparent border-0 focus:outline-none focus:ring-0 w-full truncate placeholder:text-[#8e8e93]"
            placeholder="Untitled carousel" @blur="saveTitle" />
          <div v-else class="h-4 bg-[#d1d1d6] rounded-lg animate-pulse w-40" />
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <span v-if="carousel" :class="`tag tag-${carousel.status}`">{{ carousel.status }}</span>

          <button v-if="carousel && (carousel.status === 'ready' || carousel.status === 'failed')"
            class="btn-secondary text-xs px-3 py-1.5 gap-1.5" :disabled="generating" @click="handleRegenerate">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Regenerate
          </button>

          <button v-if="carousel"
            class="btn-primary text-xs px-3 py-1.5 gap-1.5"
            :disabled="exporting || carousel.status !== 'ready'"
            :title="carousel.status !== 'ready' ? 'Generate slides first to enable export' : ''"
            @click="handleExport">
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
    <div v-if="generating || carousel?.status === 'generating'"
      class="shrink-0 bg-amber-50/90 backdrop-blur-sm border-b border-amber-200/60 px-5 py-2.5 flex items-center gap-3">
      <div class="w-4 h-4 border-2 border-amber-500 border-t-transparent rounded-full animate-spin shrink-0" />
      <span class="text-sm text-amber-800 font-medium">Generating slides with AI…</span>
    </div>

    <!-- Main layout -->
    <div v-if="carousel" class="flex flex-1 overflow-hidden">
      <div class="flex flex-col lg:flex-row w-full flex-1 overflow-hidden">

        <!-- Slide list sidebar -->
        <div class="shrink-0 bg-[#f7f7f8] border-b lg:border-b-0 lg:border-r border-black/[0.07]
                    h-[100px] lg:h-auto lg:w-[112px]
                    overflow-x-auto lg:overflow-x-hidden lg:overflow-y-auto">
          <div class="flex lg:flex-col gap-2 p-2 min-w-max lg:min-w-0">
            <button v-for="(slide, i) in slides" :key="slide.id"
              class="relative shrink-0 rounded-xl overflow-hidden border-2 transition-all duration-150 w-[68px] lg:w-full"
              :class="activeIndex === i
                ? 'border-[#0071e3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
                : 'border-[#e5e5ea] hover:border-[#c6c6c8]'"
              @click="activeIndex = i">
              <SlidePreview :slide="slide" :design="design" :small="true" />
              <div class="absolute bottom-0 inset-x-0 h-5 flex items-center justify-center
                          bg-gradient-to-t from-black/60 to-transparent">
                <span class="text-white text-[9px] font-bold">{{ i + 1 }}</span>
              </div>
            </button>
            <div v-if="slides.length === 0 && !generating"
              class="flex flex-col items-center justify-center py-6 text-[#8e8e93] text-[10px] text-center gap-1 lg:w-full w-16">
              <svg class="w-5 h-5 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              No slides
            </div>
          </div>
        </div>

        <!-- Center -->
        <div class="flex-1 flex flex-col lg:flex-row overflow-hidden">
          <div class="flex-1 py-6 px-4 lg:px-8 flex items-start justify-center overflow-y-auto">

            <div v-if="generating || carousel.status === 'generating'" class="text-center">
              <div class="w-14 h-14 border-[3px] border-[#0071e3]/20 border-t-[#0071e3] rounded-full animate-spin mx-auto mb-5" />
              <p class="text-[#3a3a3c] font-medium">Generating your slides…</p>
              <p class="text-[#8e8e93] text-sm mt-1">This takes about 15–30 seconds</p>
            </div>

            <div v-else-if="slides.length === 0" class="text-center">
              <div class="w-16 h-16 bg-white rounded-3xl shadow-[0_4px_24px_rgba(0,0,0,0.08)] flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-[#8e8e93]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <p class="text-[#3a3a3c] font-medium mb-1">No slides yet</p>
              <p class="text-[#8e8e93] text-sm">Generate slides to get started</p>
            </div>

            <div v-else class="w-full max-w-xs">
              <SlidePreview :slide="activeSlide" :design="design"
                :slide-number="activeIndex + 1" :total-slides="slides.length" :show-counter="true" />

              <!-- Editor card -->
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
                  <label class="label">CTA <span class="text-[#8e8e93] normal-case font-normal tracking-normal ml-1">— optional</span></label>
                  <input v-model="editCta" class="input" placeholder="e.g., Save this post ↓" @blur="saveSlide" />
                </div>

                <div class="border-t border-[#f2f2f7]" />

                <!-- Per-slide background -->
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <label class="label mb-0">Slide Background</label>
                    <button v-if="hasOverride" class="text-[11px] text-[#ff3b30] font-semibold hover:underline"
                      @click="clearOverride">
                      Reset to global
                    </button>
                  </div>

                  <div class="flex items-center gap-2.5 mb-3">
                    <div class="relative shrink-0">
                      <div class="w-9 h-9 rounded-xl border border-[#c6c6c8] overflow-hidden cursor-pointer shadow-sm">
                        <input type="color" :value="editOverrideBgColor || '#ffffff'"
                          class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                          @input="editOverrideBgColor = ($event.target as HTMLInputElement).value"
                          @change="saveSlide" />
                        <div class="w-full h-full" :style="{ backgroundColor: editOverrideBgColor || design.bg_color }" />
                      </div>
                    </div>
                    <input v-model="editOverrideBgColor" class="input font-mono text-sm flex-1"
                      placeholder="Use global color" @blur="saveSlide" />
                  </div>

                  <input type="file" accept="image/*" ref="slideFileInput" class="hidden" @change="handleSlideImageUpload" />
                  <button class="btn-secondary w-full text-sm gap-2 mb-2"
                    :disabled="uploadingSlide"
                    @click="(slideFileInput as HTMLInputElement)?.click()">
                    <svg v-if="uploadingSlide" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ uploadingSlide ? 'Uploading…' : 'Upload Photo for This Slide' }}
                  </button>

                  <div v-if="editOverrideBgImage" class="flex items-center gap-2.5 mb-3">
                    <img :src="editOverrideBgImage" class="w-12 h-12 object-cover rounded-xl border border-[#e5e5ea]" />
                    <button class="text-xs text-[#ff3b30] font-semibold hover:underline"
                      @click="editOverrideBgImage = null; saveSlide()">Remove photo</button>
                  </div>

                  <div v-if="editOverrideBgImage">
                    <div class="flex items-center justify-between mb-1.5">
                      <label class="label mb-0">Darkening</label>
                      <span class="text-xs text-[#0071e3] font-semibold">{{ Math.round((editOverrideDarkening ?? 0) * 100) }}%</span>
                    </div>
                    <input type="range" :value="editOverrideDarkening ?? 0" min="0" max="0.9" step="0.05"
                      @input="editOverrideDarkening = parseFloat(($event.target as HTMLInputElement).value)"
                      @change="saveSlide" />
                  </div>
                </div>

                <div v-if="saveError" class="text-[11px] text-[#ff3b30] text-right">{{ saveError }}</div>
                <div v-else-if="savingSlide" class="text-[11px] text-[#8e8e93] text-right">Saving…</div>
              </div>

              <!-- Navigation -->
              <div class="flex items-center justify-between mt-3">
                <button class="btn-secondary text-sm px-3 py-1.5 gap-1.5"
                  :disabled="activeIndex === 0" @click="activeIndex--">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                  Prev
                </button>
                <span class="text-sm text-[#3a3a3c] font-medium tabular-nums">{{ activeIndex + 1 }} / {{ slides.length }}</span>
                <button class="btn-secondary text-sm px-3 py-1.5 gap-1.5"
                  :disabled="activeIndex === slides.length - 1" @click="activeIndex++">
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
            <DesignPanel v-model="design" :active-slide="activeSlide"
              @apply-to-all="saveDesign"
              @update:slide-overrides="onSlideOverrides" />
          </div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-else class="flex-1 flex items-center justify-center">
      <div class="w-10 h-10 border-[3px] border-[#0071e3]/20 border-t-[#0071e3] rounded-full animate-spin" />
    </div>

    <!-- Export toast -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="translate-y-4 opacity-0 scale-95"
        enter-to-class="translate-y-0 opacity-100 scale-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="translate-y-0 opacity-100 scale-100"
        leave-to-class="translate-y-4 opacity-0 scale-95"
      >
        <div v-if="exportUrl"
          class="fixed bottom-6 right-6 bg-white/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_40px_rgba(0,0,0,0.15)] border border-white/50 p-4 flex items-center gap-3 z-50 max-w-sm">
          <div class="w-9 h-9 bg-[#34c759]/10 rounded-xl flex items-center justify-center shrink-0">
            <svg class="w-4 h-4 text-[#34c759]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-[#1c1c1e]">Export ready!</p>
            <p class="text-xs text-[#3a3a3c] mt-0.5">Your ZIP is ready to download</p>
          </div>
          <a :href="exportUrl" download class="btn-primary text-xs px-3 py-1.5">Download</a>
          <button class="w-6 h-6 flex items-center justify-center rounded-full text-[#8e8e93] hover:text-[#3a3a3c] hover:bg-black/5 transition-colors text-lg leading-none"
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
const uploadingSlide = ref(false)
const slideFileInput = ref<HTMLInputElement>()

const editTitle = ref("")
const editBody = ref("")
const editCta = ref("")
const editOverrideBgColor = ref("")
const editOverrideBgImage = ref<string | null>(null)
const editOverrideDarkening = ref<number | null>(null)
// Per-slide style overrides
const editOverrideTemplate = ref<string | null>(null)
const editOverrideAccent = ref<string | null>(null)
const editOverrideTitleHighlight = ref<string | null>(null)
const editOverrideAlignH = ref<string | null>(null)
const editOverrideAlignV = ref<string | null>(null)
const editOverridePattern = ref<string | null>(null)
const editOverridePatternColor = ref<string | null>(null)
const editOverridePatternOpacity = ref<number | null>(null)
// Per-slide layout overrides
const editOverridePadding = ref<number | null>(null)
const editOverrideShowHeader = ref<boolean | null>(null)
const editOverrideHeaderText = ref<string | null>(null)
const editOverrideShowFooter = ref<boolean | null>(null)
const editOverrideFooterText = ref<string | null>(null)

const activeSlide = computed(() => slides.value[activeIndex.value] ?? null)

const hasOverride = computed(() => {
  const o = activeSlide.value?.overrides
  if (!o) return false
  return !!(o.bg_color || o.bg_image_url || o.darkening != null ||
    o.template || o.accent_color || o.title_highlight || o.align_h || o.align_v ||
    o.pattern || o.pattern_color || o.pattern_opacity != null ||
    o.padding != null || o.show_header != null || o.show_footer != null)
})

const syncEditorFromSlide = (s: Slide | null) => {
  if (!s) return
  editTitle.value = s.title
  editBody.value = s.body
  editCta.value = s.footer_cta || ""
  editOverrideBgColor.value = s.overrides?.bg_color || ""
  editOverrideBgImage.value = s.overrides?.bg_image_url || null
  editOverrideDarkening.value = s.overrides?.darkening ?? null
  editOverrideTemplate.value = s.overrides?.template || null
  editOverrideAccent.value = s.overrides?.accent_color || null
  editOverrideTitleHighlight.value = s.overrides?.title_highlight || null
  editOverrideAlignH.value = s.overrides?.align_h || null
  editOverrideAlignV.value = s.overrides?.align_v || null
  editOverridePattern.value = s.overrides?.pattern || null
  editOverridePatternColor.value = s.overrides?.pattern_color || null
  editOverridePatternOpacity.value = s.overrides?.pattern_opacity ?? null
  editOverridePadding.value = s.overrides?.padding ?? null
  editOverrideShowHeader.value = s.overrides?.show_header ?? null
  editOverrideHeaderText.value = s.overrides?.header_text ?? null
  editOverrideShowFooter.value = s.overrides?.show_footer ?? null
  editOverrideFooterText.value = s.overrides?.footer_text ?? null
}

watch(activeSlide, syncEditorFromSlide)

let designLoaded = false
let designSaveTimer: ReturnType<typeof setTimeout> | null = null
watch(design, (d) => {
  if (!designLoaded) return
  if (designSaveTimer) clearTimeout(designSaveTimer)
  designSaveTimer = setTimeout(() => { saveDesign(d) }, 800)
}, { deep: true })

const loadData = async () => {
  const [c, sl] = await Promise.all([
    fetchCarousel(carouselId),
    $fetch<Slide[]>(`${config.public.apiBase}/carousels/${carouselId}/slides`),
  ])
  carousel.value = c
  slides.value = sl
  editableTitle.value = c.title
  design.value = { ...DEFAULT_DESIGN, ...c.design }
  syncEditorFromSlide(sl[0] ?? null)
  designLoaded = true
}

const saveTitle = async () => {
  if (!carousel.value || editableTitle.value === carousel.value.title) return
  await updateCarousel(carouselId, { title: editableTitle.value })
}

const saveError = ref<string | null>(null)

const saveSlide = async () => {
  const slide = activeSlide.value
  if (!slide) return
  savingSlide.value = true
  saveError.value = null
  try {
    const overrides: Record<string, any> = {}
    if (editOverrideBgColor.value) overrides.bg_color = editOverrideBgColor.value
    if (editOverrideBgImage.value) overrides.bg_image_url = editOverrideBgImage.value
    if (editOverrideDarkening.value != null) overrides.darkening = editOverrideDarkening.value
    if (editOverrideTemplate.value) overrides.template = editOverrideTemplate.value
    if (editOverrideAccent.value) overrides.accent_color = editOverrideAccent.value
    if (editOverrideTitleHighlight.value) overrides.title_highlight = editOverrideTitleHighlight.value
    if (editOverrideAlignH.value) overrides.align_h = editOverrideAlignH.value
    if (editOverrideAlignV.value) overrides.align_v = editOverrideAlignV.value
    if (editOverridePattern.value) overrides.pattern = editOverridePattern.value
    if (editOverridePatternColor.value) overrides.pattern_color = editOverridePatternColor.value
    if (editOverridePatternOpacity.value != null) overrides.pattern_opacity = editOverridePatternOpacity.value
    if (editOverridePadding.value != null) overrides.padding = editOverridePadding.value
    if (editOverrideShowHeader.value != null) overrides.show_header = editOverrideShowHeader.value
    if (editOverrideHeaderText.value != null) overrides.header_text = editOverrideHeaderText.value
    if (editOverrideShowFooter.value != null) overrides.show_footer = editOverrideShowFooter.value
    if (editOverrideFooterText.value != null) overrides.footer_text = editOverrideFooterText.value

    const updated = await $fetch<Slide>(
      `${config.public.apiBase}/carousels/${carouselId}/slides/${slide.id}`,
      { method: "PATCH", body: { title: editTitle.value, body: editBody.value, footer_cta: editCta.value || null, overrides } }
    )
    slides.value[activeIndex.value] = updated
  } catch (e: any) {
    saveError.value = e?.data?.detail || "Failed to save slide"
  } finally {
    savingSlide.value = false
  }
}

const clearOverride = async () => {
  editOverrideBgColor.value = ""
  editOverrideBgImage.value = null
  editOverrideDarkening.value = null
  editOverrideTemplate.value = null
  editOverrideAccent.value = null
  editOverrideTitleHighlight.value = null
  editOverrideAlignH.value = null
  editOverrideAlignV.value = null
  editOverridePattern.value = null
  editOverridePatternColor.value = null
  editOverridePatternOpacity.value = null
  editOverridePadding.value = null
  editOverrideShowHeader.value = null
  editOverrideHeaderText.value = null
  editOverrideShowFooter.value = null
  editOverrideFooterText.value = null
  await saveSlide()
}

// Called by DesignPanel when slide style overrides change
const onSlideOverrides = async (ov: import("~/types").SlideOverrides) => {
  editOverrideTemplate.value = ov.template ?? null
  editOverrideAccent.value = ov.accent_color ?? null
  editOverrideTitleHighlight.value = ov.title_highlight ?? null
  editOverrideAlignH.value = ov.align_h ?? null
  editOverrideAlignV.value = ov.align_v ?? null
  editOverridePattern.value = ov.pattern ?? null
  editOverridePatternColor.value = ov.pattern_color ?? null
  editOverridePatternOpacity.value = ov.pattern_opacity ?? null
  editOverridePadding.value = ov.padding ?? null
  editOverrideShowHeader.value = ov.show_header ?? null
  editOverrideHeaderText.value = ov.header_text ?? null
  editOverrideShowFooter.value = ov.show_footer ?? null
  editOverrideFooterText.value = ov.footer_text ?? null
  await saveSlide()
}

const handleSlideImageUpload = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploadingSlide.value = true
  try {
    const form = new FormData()
    form.append("file", file)
    const resp = await $fetch<{ url: string }>(`${config.public.apiBase}/assets/upload`, { method: "POST", body: form })
    editOverrideBgImage.value = resp.url
    await saveSlide()
  } catch (e: any) {
    saveError.value = e?.data?.detail || "Upload failed. Check file type and size."
  } finally {
    uploadingSlide.value = false
    if (slideFileInput.value) slideFileInput.value.value = ""
  }
}

const saveDesign = async (d: CarouselDesign) => {
  savingDesign.value = true
  try {
    const updated = await updateDesign(carouselId, d)
    carousel.value = updated
    designLoaded = false
    design.value = { ...DEFAULT_DESIGN, ...updated.design }
    designLoaded = true
  } finally { savingDesign.value = false }
}

const startPollGeneration = (genId: string) => {
  generating.value = true
  if (carousel.value) carousel.value.status = "generating"
  pollGeneration(genId,
    async () => { generating.value = false; await loadData() },
    () => { generating.value = false; if (carousel.value) carousel.value.status = "failed" }
  )
}

const handleRegenerate = async () => {
  if (!confirm("Regenerate slides? Your current slide text edits will be replaced.")) return
  startPollGeneration((await startGeneration(carouselId)).id)
}

const handleExport = async () => {
  exporting.value = true
  exportStatus.value = "Queuing…"
  try {
    const exp = await startExport(carouselId)
    exportStatus.value = "Rendering…"
    pollExport(exp.id,
      (done) => { exporting.value = false; if (done.file_url) exportUrl.value = done.file_url },
      (failed) => {
        exporting.value = false
        const reason = (failed as any)?.error
        alert(reason ? `Export failed: ${reason}` : "Export failed. Please try again.")
      }
    )
  } catch { exporting.value = false; alert("Export failed.") }
}

onMounted(async () => {
  await loadData()
  if (genIdFromQuery) startPollGeneration(genIdFromQuery)
})
</script>
