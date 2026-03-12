<template>
  <div class="h-[100dvh] bg-[#F4F5F6] flex flex-col overflow-hidden relative">
    <ToastContainer />
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/90 backdrop-blur-xl border-b border-[#E6E8EA] shrink-0">
      <div class="px-3 sm:px-4 h-14 flex items-center gap-2 sm:gap-3">
        <NuxtLink to="/dashboard"
          class="w-8 h-8 rounded-xl flex items-center justify-center text-[#3a3a3c] hover:bg-black/5 transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </NuxtLink>

        <div class="flex-1 min-w-0">
          <input v-if="carousel" v-model="editableTitle"
            class="font-semibold text-[#000000] text-sm bg-transparent border-0 focus:outline-none focus:ring-0 w-full truncate placeholder:text-[#8e8e93]"
            placeholder="Untitled carousel" @blur="saveTitle" />
          <div v-else class="h-4 bg-[#d1d1d6] rounded-lg animate-pulse w-40" />
        </div>

        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
          <span v-if="carousel" :class="`tag tag-${carousel.status} hidden sm:inline-flex`">{{ carousel.status }}</span>

          <!-- Generation history button -->
          <button v-if="carousel"
            class="w-8 h-8 rounded-xl flex items-center justify-center text-[#3a3a3c] hover:bg-black/5 transition-colors"
            title="Generation history" aria-label="View generation history" @click="showHistory = true">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>

          <button v-if="carousel && (carousel.status === 'ready' || carousel.status === 'failed')"
            class="btn-secondary text-xs px-2 sm:px-3 py-1.5 gap-1.5" :disabled="generating" @click="handleRegenerate">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span class="hidden sm:inline">Regenerate</span>
          </button>

          <button v-if="carousel"
            class="btn-primary text-xs px-2 sm:px-3 py-1.5 gap-1.5"
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
            <span class="hidden sm:inline">{{ exporting ? exportStatus : 'Export ZIP' }}</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Generation banner -->
    <div v-if="generating || carousel?.status === 'generating'"
      class="shrink-0 bg-amber-50/90 backdrop-blur-sm border-b border-amber-200/60 px-4 py-2 flex items-center gap-3">
      <div class="w-4 h-4 border-2 border-amber-500 border-t-transparent rounded-full animate-spin shrink-0" />
      <span class="text-sm text-amber-800 font-medium">Generating slides with AI…</span>
    </div>

    <!-- Single file input shared across layouts -->
    <input type="file" accept="image/*" ref="slideFileInput" class="hidden" @change="handleSlideImageUpload" />

    <!-- Main layout -->
    <div v-if="carousel" class="flex flex-1 overflow-hidden">

      <!-- ── DESKTOP layout (lg+) ── -->
      <div class="hidden lg:flex w-full flex-1 overflow-hidden">

        <!-- Slide list sidebar -->
        <div class="shrink-0 bg-[#f7f7f8] border-r border-black/[0.07] w-[112px] overflow-y-auto">
          <div class="flex flex-col gap-2 p-2">
            <div v-for="(slide, i) in slides" :key="slide.id" class="group relative w-full">
              <button
                class="relative shrink-0 rounded-xl overflow-hidden border-2 transition-all duration-150 w-full"
                :class="activeIndex === i
                  ? 'border-[#2B31B3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
                  : 'border-[#e5e5ea] hover:border-[#c6c6c8]'"
                :aria-label="`Select slide ${i + 1}`"
                @click="activeIndex = i">
                <div class="w-full overflow-hidden">
                  <div style="width: 320px; transform-origin: top left;" :style="thumbnailScaleStyle">
                    <SlidePreview :slide="slide" :design="design" />
                  </div>
                </div>
                <div class="absolute bottom-0 inset-x-0 h-5 flex items-center justify-center
                            bg-gradient-to-t from-black/60 to-transparent">
                  <span class="text-white text-[9px] font-bold">{{ i + 1 }}</span>
                </div>
              </button>
              <!-- Slide controls (visible on hover or when active) -->
              <div class="absolute top-1 right-1 flex flex-col gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                <button class="w-5 h-5 bg-white/90 rounded-md flex items-center justify-center shadow-sm disabled:opacity-30"
                  :disabled="i === 0" :aria-label="`Move slide ${i + 1} up`"
                  @click.stop="handleMoveSlide(slide.id, 'up')">
                  <svg class="w-3 h-3 text-[#000000]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
                <button class="w-5 h-5 bg-white/90 rounded-md flex items-center justify-center shadow-sm disabled:opacity-30"
                  :disabled="i === slides.length - 1" :aria-label="`Move slide ${i + 1} down`"
                  @click.stop="handleMoveSlide(slide.id, 'down')">
                  <svg class="w-3 h-3 text-[#000000]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <button class="w-5 h-5 bg-white/90 rounded-md flex items-center justify-center shadow-sm hover:bg-red-50"
                  :aria-label="`Delete slide ${i + 1}`"
                  @click.stop="handleDeleteSlide(slide.id)">
                  <svg class="w-3 h-3 text-[#ff3b30]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            <div v-if="slides.length === 0 && !generating"
              class="flex flex-col items-center justify-center py-6 text-[#8e8e93] text-[10px] text-center gap-1">
              <svg class="w-5 h-5 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              No slides
            </div>
          </div>
        </div>

        <!-- Center + Design panel -->
        <div class="flex-1 flex overflow-hidden">
          <div class="flex-1 py-6 px-8 flex items-start justify-center overflow-y-auto">
            <div v-if="generating || carousel.status === 'generating'" class="text-center mt-20">
              <div class="w-14 h-14 border-[3px] border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin mx-auto mb-5" />
              <p class="text-[#3a3a3c] font-medium">Generating your slides…</p>
              <p class="text-[#8e8e93] text-sm mt-1">This takes about 15–30 seconds</p>
            </div>
            <div v-else-if="slides.length === 0" class="text-center mt-20">
              <p class="text-[#3a3a3c] font-medium mb-1">No slides yet</p>
              <p class="text-[#8e8e93] text-sm">Generate slides to get started</p>
            </div>
            <div v-else class="w-full max-w-xs">
              <div class="relative" ref="slidePreviewRef" @mouseup="onPreviewMouseUp">
                <SlidePreview :slide="activeSlide" :design="design"
                  :slide-number="activeIndex + 1" :total-slides="slides.length" :show-counter="true" />
              </div>
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
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <label class="label mb-0">Slide Background</label>
                    <button v-if="hasOverride" class="text-[11px] text-[#ff3b30] font-semibold hover:underline"
                      @click="clearOverride">Reset to global</button>
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
                  <button class="btn-secondary w-full text-sm gap-2 mb-2" :disabled="uploadingSlide"
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
                      <span class="text-xs text-[#2B31B3] font-semibold">{{ Math.round((editOverrideDarkening ?? 0) * 100) }}%</span>
                    </div>
                    <input type="range" :value="editOverrideDarkening ?? 0" min="0" max="0.9" step="0.05"
                      @input="editOverrideDarkening = parseFloat(($event.target as HTMLInputElement).value)"
                      @change="saveSlide" />
                  </div>
                </div>
                <div v-if="saveError" class="text-[11px] text-[#ff3b30] text-right">{{ saveError }}</div>
                <div v-else-if="savingSlide" class="text-[11px] text-[#8e8e93] text-right">Saving…</div>
              </div>
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
          <div class="w-72 shrink-0 bg-white border-l border-black/[0.06] flex flex-col overflow-hidden">
            <DesignPanel v-model="design" :active-slide="activeSlide"
              @apply-to-all="saveDesign"
              @update:slide-overrides="onSlideOverrides" />
          </div>
        </div>
      </div>

      <!-- ── MOBILE layout (<lg) ── -->
      <div class="flex lg:hidden flex-col w-full flex-1 overflow-hidden">

        <!-- Mobile content area (switches by mobileTab) -->
        <div class="flex-1 overflow-hidden">

          <!-- SLIDES tab: horizontal strip + preview -->
          <div v-if="mobileTab === 'slides'" class="h-full flex flex-col overflow-hidden">
            <!-- Horizontal slide strip -->
            <div class="shrink-0 bg-[#f7f7f8] border-b border-black/[0.07] overflow-x-auto">
              <div class="flex gap-2 p-2 min-w-max">
                <button v-for="(slide, i) in slides" :key="slide.id"
                  class="relative shrink-0 rounded-xl overflow-hidden border-2 transition-all duration-150"
                  :class="activeIndex === i
                    ? 'border-[#2B31B3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
                    : 'border-[#e5e5ea]'"
                  :style="thumbnailScaleStyleMobile.container"
                  @click="activeIndex = i">
                  <div :style="thumbnailScaleStyleMobile.inner">
                    <SlidePreview :slide="slide" :design="design" />
                  </div>
                  <div class="absolute bottom-0 inset-x-0 h-4 flex items-center justify-center
                              bg-gradient-to-t from-black/60 to-transparent">
                    <span class="text-white text-[8px] font-bold">{{ i + 1 }}</span>
                  </div>
                </button>
              </div>
            </div>

            <!-- Active slide preview -->
            <div class="flex-1 overflow-y-auto py-4 px-4 flex flex-col items-center">
              <div v-if="generating || carousel.status === 'generating'" class="text-center mt-8">
                <div class="w-10 h-10 border-[3px] border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin mx-auto mb-4" />
                <p class="text-[#3a3a3c] font-medium text-sm">Generating…</p>
              </div>
              <div v-else-if="slides.length > 0" class="w-full max-w-[260px]">
                <div class="relative" ref="slidePreviewRefMobile" @mouseup="onPreviewMouseUp">
                  <SlidePreview :slide="activeSlide" :design="design"
                    :slide-number="activeIndex + 1" :total-slides="slides.length" :show-counter="true" />
                </div>
                <div class="flex items-center justify-between mt-3">
                  <button class="btn-secondary text-xs px-3 py-1.5 gap-1"
                    :disabled="activeIndex === 0" @click="activeIndex--">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Prev
                  </button>
                  <span class="text-xs text-[#3a3a3c] font-medium tabular-nums">{{ activeIndex + 1 }} / {{ slides.length }}</span>
                  <button class="btn-secondary text-xs px-3 py-1.5 gap-1"
                    :disabled="activeIndex === slides.length - 1" @click="activeIndex++">
                    Next
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- EDIT tab: text + bg editor -->
          <div v-else-if="mobileTab === 'edit'" class="h-full overflow-y-auto">
            <div v-if="slides.length > 0" class="p-4 space-y-4">
              <div class="card p-5 space-y-4">
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
                <!-- Slide background -->
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <label class="label mb-0">Slide Background</label>
                    <button v-if="hasOverride" class="text-[11px] text-[#ff3b30] font-semibold hover:underline"
                      @click="clearOverride">Reset to global</button>
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
                  <button class="btn-secondary w-full text-sm gap-2 mb-2" :disabled="uploadingSlide"
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
                      <span class="text-xs text-[#2B31B3] font-semibold">{{ Math.round((editOverrideDarkening ?? 0) * 100) }}%</span>
                    </div>
                    <input type="range" :value="editOverrideDarkening ?? 0" min="0" max="0.9" step="0.05"
                      @input="editOverrideDarkening = parseFloat(($event.target as HTMLInputElement).value)"
                      @change="saveSlide" />
                  </div>
                </div>
                <div v-if="saveError" class="text-[11px] text-[#ff3b30] text-right">{{ saveError }}</div>
                <div v-else-if="savingSlide" class="text-[11px] text-[#8e8e93] text-right">Saving…</div>
              </div>
            </div>
            <div v-else class="flex items-center justify-center h-full text-[#8e8e93] text-sm">
              Generate slides to start editing
            </div>
          </div>

          <!-- DESIGN tab: slide preview + DesignPanel -->
          <div v-else-if="mobileTab === 'design'" class="h-full bg-white flex flex-col overflow-hidden">
            <!-- Mini preview strip -->
            <div v-if="activeSlide" class="shrink-0 bg-[#f7f7f8] border-b border-black/[0.07] px-4 py-3 flex justify-center">
              <div class="w-[120px]">
                <SlidePreview :slide="activeSlide" :design="design"
                  :slide-number="activeIndex + 1" :total-slides="slides.length" />
              </div>
            </div>
            <DesignPanel v-model="design" :active-slide="activeSlide"
              @apply-to-all="saveDesign"
              @update:slide-overrides="onSlideOverrides" />
          </div>
        </div>

        <!-- Mobile bottom tab bar -->
        <nav class="shrink-0 bg-white/90 backdrop-blur-xl border-t border-black/[0.06] flex safe-area-inset-bottom">
          <button v-for="tab in mobileTabs" :key="tab.key"
            class="flex-1 flex flex-col items-center gap-0.5 py-2.5 transition-colors"
            :class="mobileTab === tab.key ? 'text-[#2B31B3]' : 'text-[#8e8e93]'"
            @click="mobileTab = tab.key">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="tab.icon" />
            </svg>
            <span class="text-[10px] font-medium">{{ tab.label }}</span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Loading state -->
    <div v-else class="flex-1 flex items-center justify-center">
      <div class="w-10 h-10 border-[3px] border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin" />
    </div>

    <!-- Generation history panel -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="showHistory" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:p-4"
          @click.self="showHistory = false">
          <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" @click="showHistory = false" />
          <div class="relative bg-white rounded-t-2xl sm:rounded-2xl w-full sm:max-w-md max-h-[80dvh] flex flex-col shadow-2xl">
            <!-- Header -->
            <div class="flex items-center justify-between px-5 py-4 border-b border-[#f2f2f7] shrink-0">
              <h2 class="font-semibold text-[#000000] text-sm">Generation History</h2>
              <button class="w-7 h-7 rounded-full flex items-center justify-center text-[#8e8e93] hover:bg-black/5 transition-colors"
                @click="showHistory = false">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <!-- List -->
            <div class="flex-1 overflow-y-auto px-5 py-3 space-y-2">
              <div v-if="historyLoading" class="flex items-center justify-center py-8">
                <div class="w-6 h-6 border-2 border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin" />
              </div>
              <div v-else-if="historyError" class="text-sm text-[#ff3b30] text-center py-6">{{ historyError }}</div>
              <div v-else-if="generationHistory.length === 0" class="text-sm text-[#8e8e93] text-center py-6">No generations yet</div>
              <div v-for="gen in generationHistory" :key="gen.id"
                class="rounded-xl border border-[#f2f2f7] bg-[#f9f9fb] px-4 py-3 flex items-start gap-3">
                <!-- Status dot -->
                <div class="mt-0.5 w-2 h-2 rounded-full shrink-0" :class="{
                  'bg-[#34c759]': gen.status === 'done',
                  'bg-[#ff3b30]': gen.status === 'failed',
                  'bg-[#ff9500]': gen.status === 'running',
                  'bg-[#8e8e93]': gen.status === 'queued',
                }" />
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs font-semibold" :class="{
                      'text-[#34c759]': gen.status === 'done',
                      'text-[#ff3b30]': gen.status === 'failed',
                      'text-[#ff9500]': gen.status === 'running',
                      'text-[#8e8e93]': gen.status === 'queued',
                    }">{{ gen.status }}</span>
                    <span v-if="gen.tokens_used" class="text-[11px] text-[#8e8e93]">{{ gen.tokens_used.toLocaleString() }} tokens</span>
                  </div>
                  <div class="text-[11px] text-[#8e8e93] mt-0.5">{{ formatRelativeTime(gen.created_at) }}</div>
                  <div v-if="gen.error" class="text-[11px] text-[#ff3b30] mt-1 truncate" :title="gen.error">{{ gen.error }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Floating highlight toolbar -->
    <Teleport to="body">
      <div v-if="floatingToolbar.visible"
        ref="floatingToolbarEl"
        class="fixed z-[100] flex items-center gap-0.5 bg-[#000000]/95 backdrop-blur-sm rounded-xl shadow-xl px-1 py-1 pointer-events-auto"
        :style="{ left: floatingToolbar.x + 'px', top: floatingToolbar.y + 'px', transform: 'translateX(-50%)' }">

        <!-- Highlight color swatches -->
        <div class="flex items-center gap-1 px-1" title="Highlight background color">
          <div class="relative w-5 h-5 rounded cursor-pointer border border-white/20 overflow-hidden shrink-0"
            :style="{ background: hlBgColor || accentForToolbar }">
            <input type="color" :value="hlBgColor || accentForToolbar"
              class="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
              @input="hlBgColor = ($event.target as HTMLInputElement).value" />
          </div>
          <div class="relative w-5 h-5 rounded cursor-pointer border border-white/20 overflow-hidden shrink-0"
            :style="{ background: hlTextColor }"
            title="Highlight text color">
            <input type="color" :value="hlTextColor"
              class="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
              @input="hlTextColor = ($event.target as HTMLInputElement).value" />
          </div>
        </div>
        <div class="w-px h-4 bg-white/20" />

        <button
          class="flex items-center gap-1 px-2 py-1 rounded-lg text-[11px] font-semibold text-white hover:bg-white/10 transition-colors"
          title="Highlight selected text"
          @click="applyHighlight">
          <span class="px-1 rounded text-[10px] font-bold"
            :style="{ background: hlBgColor || accentForToolbar, color: hlTextColor }">A</span>
          Highlight
        </button>
        <div class="w-px h-4 bg-white/20" />
        <button
          class="flex items-center gap-1 px-2 py-1 rounded-lg text-[11px] font-bold text-white hover:bg-white/10 transition-colors"
          title="Bold"
          @click="applyBold">
          <b class="text-[11px]">B</b>
        </button>
      </div>
    </Teleport>

    <!-- Export screen overlay -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-2"
    >
      <div v-if="exportUrl" class="absolute inset-0 z-40 bg-[#F4F5F6] flex flex-col overflow-hidden">
        <!-- Export header -->
        <div class="shrink-0 bg-white border-b border-[#E6E8EA] px-4 sm:px-6 h-14 flex items-center gap-3">
          <h1 class="font-bold text-[#000000] text-base flex-1">{{ t.exportReady }}</h1>
          <button
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#e5e5ea] bg-white text-[#8e8e93] text-sm font-medium hover:bg-[#f7f7f8] hover:text-[#3a3a3c] transition-colors"
            :disabled="exporting"
            @click="exportUrl = null; handleExport(true)">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ t.recreateBtn }}
          </button>
          <button
            class="btn-secondary text-sm px-3 py-1.5 gap-1.5 flex items-center"
            @click="exportUrl = null">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            {{ t.backToEditor }}
          </button>
        </div>

        <!-- Slides grid -->
        <div class="flex-1 overflow-y-auto px-4 sm:px-8 py-6">
          <div class="flex flex-wrap gap-4 sm:gap-5">
            <div v-for="(slide, i) in slides" :key="slide.id" class="flex flex-col gap-2">
              <!-- Slide preview thumbnail -->
              <div class="relative rounded-xl overflow-hidden border border-[#e5e5ea] bg-white shadow-sm"
                style="width: 180px; height: 225px;">
                <div class="overflow-hidden" style="width: 180px; height: 225px;">
                  <div :style="exportThumbnailScaleStyle">
                    <SlidePreview :slide="slide" :design="design" />
                  </div>
                </div>
                <!-- Slide number badge -->
                <div class="absolute top-1.5 left-1.5 bg-black/50 backdrop-blur-sm text-white text-[10px] font-bold px-1.5 py-0.5 rounded-md">
                  {{ i + 1 }}
                </div>
              </div>
              <!-- Per-slide download button -->
              <button
                style="width: 180px;"
                class="flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#e5e5ea] bg-white text-[#3a3a3c] text-xs font-medium hover:bg-[#f7f7f8] hover:border-[#c6c6c8] transition-all duration-150"
                @click="downloadFile(exportSlideUrls[i], `slide_${String(i + 1).padStart(2, '0')}.png`)">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                {{ t.downloadSlide }}
              </button>
            </div>
          </div>
        </div>

        <!-- Export footer -->
        <div class="shrink-0 bg-white border-t border-[#E6E8EA] px-4 sm:px-8 py-4 flex items-center justify-between gap-4">
          <p class="text-sm text-[#3a3a3c] font-medium">
            <span class="text-[#34c759] font-bold mr-1">✓</span>
            {{ t.slidesSuccess(slides.length) }}
          </p>
          <button
            class="btn-primary text-sm px-4 py-2 gap-2 flex items-center shrink-0"
            @click="downloadFile(exportUrl ?? undefined, 'slides.zip')">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ t.downloadAll }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import type { Carousel, Slide, CarouselDesign } from "~/types"
import { DEFAULT_DESIGN } from "~/types"

definePageMeta({ layout: false })

const route = useRoute()
const config = useRuntimeConfig()
const { authHeaders } = useAuth()
const { t } = useLang()
const { fetchCarousel, updateCarousel, updateDesign, fetchGenerations, deleteSlide, moveSlide } = useCarousels()
const { startGeneration, pollGeneration } = useGeneration()
const { getLatestExport, startExport, pollExport } = useExport()
const { show: showToast } = useToast()

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
const exportStatus = ref("Queuing…")
const exportUrl = ref<string | null>(null)
const exportSlideUrls = ref<string[]>([])
const design = ref<CarouselDesign>({ ...DEFAULT_DESIGN })
const uploadingSlide = ref(false)
const slideFileInput = ref<HTMLInputElement>()
const slidePreviewRef = ref<HTMLElement>()
const slidePreviewRefMobile = ref<HTMLElement>()
const floatingToolbarEl = ref<HTMLElement>()

// Floating highlight toolbar — shown when text is selected on the slide preview
const floatingToolbar = reactive({ visible: false, x: 0, y: 0, field: '' as 'title' | 'body' | '', text: '', rawStart: 0, rawEnd: 0 })
const accentForToolbar = computed(() => design.value.accent_color || '#f97316')
const hlBgColor = ref('')   // empty = use accent color
const hlTextColor = ref('#ffffff')

// Map selected text within rendered v-html back to raw string offsets.
// The rendered HTML may contain <span> tags (from ==markers==), so we strip
// all HTML tags and unescape HTML entities to get plain text, then find the
// selection within the raw source string.
function findRawOffset(raw: string, renderedSelectedText: string): { start: number; end: number } | null {
  // Strip ==...==  and **...** markers from raw to get plain visible text
  const plain = raw
    .replace(/==(#[0-9a-fA-F]{3,8}\|#[0-9a-fA-F]{3,8}\|)?(.+?)==/g, '$2')
    .replace(/\*\*(.+?)\*\*/g, '$1')
  const idx = plain.indexOf(renderedSelectedText)
  if (idx === -1) return null

  // Walk raw string mapping plain-text index back to raw index.
  // Skip over opening/closing marker tokens without advancing plainIdx.
  const colorPfxRe = /^==#[0-9a-fA-F]{3,8}\|#[0-9a-fA-F]{3,8}\|/
  let rawIdx = 0
  let plainIdx = 0
  let rawStart = -1
  let rawEnd = -1
  while (rawIdx <= raw.length) {
    if (plainIdx === idx) rawStart = rawIdx
    if (plainIdx === idx + renderedSelectedText.length) { rawEnd = rawIdx; break }
    if (rawIdx === raw.length) break
    // Skip extended ==color|color| opening marker
    const colorMatch = raw.slice(rawIdx).match(colorPfxRe)
    if (colorMatch) { rawIdx += colorMatch[0].length; continue }
    // Skip plain == closing/opening marker
    if (raw.startsWith('==', rawIdx)) { rawIdx += 2; continue }
    // Skip ** opening/closing marker
    if (raw.startsWith('**', rawIdx)) { rawIdx += 2; continue }
    rawIdx++
    plainIdx++
  }
  if (rawStart === -1 || rawEnd === -1) return null
  return { start: rawStart, end: rawEnd }
}

const onPreviewMouseUp = () => {
  const sel = window.getSelection()
  if (!sel || sel.isCollapsed || !sel.toString().trim()) {
    floatingToolbar.visible = false
    return
  }

  // Find the closest [data-field] ancestor of the selection anchor
  const anchorNode = sel.anchorNode
  const el = anchorNode instanceof Element
    ? anchorNode.closest('[data-field]')
    : anchorNode?.parentElement?.closest('[data-field]')

  if (!el) { floatingToolbar.visible = false; return }

  const field = el.getAttribute('data-field') as 'title' | 'body'
  const selectedText = sel.toString()

  const raw = field === 'title' ? editTitle.value : editBody.value
  const offsets = findRawOffset(raw, selectedText)
  if (!offsets) { floatingToolbar.visible = false; return }

  // Position above the selection
  const range = sel.getRangeAt(0)
  const rect = range.getBoundingClientRect()
  floatingToolbar.x = rect.left + rect.width / 2
  floatingToolbar.y = rect.top - 48
  floatingToolbar.visible = true
  floatingToolbar.field = field
  floatingToolbar.text = selectedText
  floatingToolbar.rawStart = offsets.start
  floatingToolbar.rawEnd = offsets.end
}

const applyWrap = (open: string, close: string) => {
  const { field, rawStart, rawEnd } = floatingToolbar
  if (!field) return
  const val = field === 'title' ? editTitle.value : editBody.value
  const newVal = val.slice(0, rawStart) + open + val.slice(rawStart, rawEnd) + close + val.slice(rawEnd)
  if (field === 'title') editTitle.value = newVal
  else editBody.value = newVal
  floatingToolbar.visible = false
  window.getSelection()?.removeAllRanges()
  nextTick(() => saveSlide())
}
const applyHighlight = () => {
  const bg = hlBgColor.value || accentForToolbar.value
  const fg = hlTextColor.value || '#ffffff'
  const isDefault = bg === accentForToolbar.value && fg === '#ffffff'
  if (isDefault) {
    applyWrap('==', '==')
  } else {
    applyWrap(`==${bg}|${fg}|`, '==')
  }
}
const applyBold = () => applyWrap('**', '**')

// Hide toolbar on any click outside (but not on the toolbar itself)
onMounted(() => {
  document.addEventListener('mousedown', (e) => {
    if (!floatingToolbar.visible) return
    // Don't hide if clicking inside the floating toolbar
    const target = e.target as Node
    if (floatingToolbarEl.value?.contains(target)) return
    floatingToolbar.visible = false
  })
})

// Generation history
const showHistory = ref(false)
const historyLoading = ref(false)
const historyError = ref<string | null>(null)
const generationHistory = ref<import("~/types").Generation[]>([])

watch(showHistory, async (open) => {
  if (!open) return
  historyLoading.value = true
  historyError.value = null
  try {
    generationHistory.value = await fetchGenerations(carouselId)
  } catch {
    historyError.value = "Failed to load history"
  } finally {
    historyLoading.value = false
  }
})

const formatRelativeTime = (iso: string) => {
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return "just now"
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return `${Math.floor(hrs / 24)}d ago`
}

// Mobile tab state
const mobileTab = ref<"slides" | "edit" | "design">("slides")
const mobileTabs = [
  { key: "slides", label: "Slides", icon: "M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" },
  { key: "edit",   label: "Edit",   icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" },
  { key: "design", label: "Design", icon: "M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" },
] as const

const editTitle = ref("")
const editBody = ref("")
const editCta = ref("")
const editOverrideBgColor = ref("")
const editOverrideBgImage = ref<string | null>(null)
const editOverrideDarkening = ref<number | null>(null)
const editOverrideTemplate = ref<string | null>(null)
const editOverrideAccent = ref<string | null>(null)
const editOverrideTitleHighlight = ref<string | null>(null)
const editOverrideAlignH = ref<string | null>(null)
const editOverrideAlignV = ref<string | null>(null)
const editOverridePattern = ref<string | null>(null)
const editOverridePatternColor = ref<string | null>(null)
const editOverridePatternOpacity = ref<number | null>(null)
const editOverridePadding = ref<number | null>(null)
const editOverrideShowHeader = ref<boolean | null>(null)
const editOverrideHeaderText = ref<string | null>(null)
const editOverrideShowFooter = ref<boolean | null>(null)
const editOverrideFooterText = ref<string | null>(null)

const activeSlide = computed(() => slides.value[activeIndex.value] ?? null)

// Thumbnail scaling — desktop: 96px wide inner, mobile: 60px
const thumbnailScaleStyle = computed(() => {
  const aspectRatio = design.value.aspect_ratio ?? "4:5"
  const [w, h] = aspectRatio === "9:16" ? [9, 16] : aspectRatio === "1:1" ? [1, 1] : [4, 5]
  const renderedW = 320
  const renderedH = renderedW * h / w
  const scale = 96 / renderedW
  return {
    transform: `scale(${scale})`,
    height: `${renderedH}px`,
    marginBottom: `${renderedH * (scale - 1)}px`,
  }
})

// Export screen thumbnails: rendered at 320px width, scaled to ~180px display width
const exportThumbnailScaleStyle = computed(() => {
  const aspectRatio = design.value.aspect_ratio ?? "4:5"
  const [w, h] = aspectRatio === "9:16" ? [9, 16] : aspectRatio === "1:1" ? [1, 1] : [4, 5]
  const renderedW = 320
  const renderedH = renderedW * h / w
  const scale = 180 / renderedW
  return {
    transform: `scale(${scale})`,
    transformOrigin: 'top left',
    width: `${renderedW}px`,
    height: `${renderedH}px`,
  }
})

const thumbnailScaleStyleMobile = computed(() => {
  const aspectRatio = design.value.aspect_ratio ?? "4:5"
  const [w, h] = aspectRatio === "9:16" ? [9, 16] : aspectRatio === "1:1" ? [1, 1] : [4, 5]
  const renderedW = 320
  const renderedH = renderedW * h / w
  const scale = 60 / renderedW
  const scaledH = Math.round(renderedH * scale)
  return {
    inner: {
      transform: `scale(${scale})`,
      transformOrigin: 'top left',
      width: `${renderedW}px`,
      height: `${renderedH}px`,
    },
    container: {
      width: '60px',
      height: `${scaledH}px`,
      overflow: 'hidden',
    },
  }
})

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
    $fetch<Slide[]>(`${config.public.apiBase}/carousels/${carouselId}/slides`, { headers: authHeaders() }),
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
      { method: "PATCH", body: { title: editTitle.value, body: editBody.value, footer_cta: editCta.value || null, overrides }, headers: authHeaders() }
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
    const resp = await $fetch<{ url: string }>(`${config.public.apiBase}/assets/upload`, { method: "POST", body: form, headers: authHeaders() })
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
  try {
    startPollGeneration((await startGeneration(carouselId)).id)
  } catch (e: any) {
    if (e?.response?.status === 429 || e?.statusCode === 429) {
      const detail = e?.data?.detail ?? e?.response?._data?.detail ?? ""
      const match = detail.match(/(\d+)/)
      const wait = match ? ` Please wait ${match[1]}s.` : ""
      showToast(`Slow down!${wait} Generation is limited to once every 30s.`, "warning")
    } else {
      showToast("Generation failed. Please try again.", "error")
    }
  }
}

const handleDeleteSlide = async (slideId: string) => {
  if (slides.value.length <= 1) { alert("Cannot delete the only slide."); return }
  if (!confirm("Delete this slide?")) return
  try {
    await deleteSlide(carouselId, slideId)
    const idx = slides.value.findIndex((s) => s.id === slideId)
    slides.value.splice(idx, 1)
    activeIndex.value = Math.min(activeIndex.value, slides.value.length - 1)
  } catch { alert("Failed to delete slide.") }
}

const handleMoveSlide = async (slideId: string, direction: "up" | "down") => {
  const idx = slides.value.findIndex((s) => s.id === slideId)
  const newOrder = direction === "up" ? idx - 1 : idx + 1
  if (newOrder < 0 || newOrder >= slides.value.length) return
  try {
    slides.value = await moveSlide(carouselId, slideId, newOrder)
    activeIndex.value = newOrder
  } catch { alert("Failed to reorder slide.") }
}

const downloadFile = async (url: string | undefined, filename: string) => {
  if (!url) return
  const blob = await fetch(url).then((r) => r.blob())
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = filename
  a.click()
  URL.revokeObjectURL(a.href)
}

const handleExport = async (forceNew = false) => {
  // Reuse last completed export unless force-refreshing
  if (!forceNew) {
    const latest = await getLatestExport(carouselId)
    if (latest?.file_url) {
      exportUrl.value = latest.file_url
      exportSlideUrls.value = latest.slide_urls ?? []
      return
    }
  }

  exporting.value = true
  exportStatus.value = "Queuing…"
  try {
    const exp = await startExport(carouselId)
    let frame = 0
    const frames = ["Rendering…", "Rendering.", "Rendering..", "Rendering..."]
    const timer = setInterval(() => { frame = (frame + 1) % frames.length; exportStatus.value = frames[frame] }, 600)
    pollExport(exp.id,
      (done) => { clearInterval(timer); exporting.value = false; if (done.file_url) { exportUrl.value = done.file_url; exportSlideUrls.value = done.slide_urls ?? [] } },
      (failed) => {
        clearInterval(timer); exporting.value = false
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
