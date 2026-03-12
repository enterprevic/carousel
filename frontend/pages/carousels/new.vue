<template>
  <div class="h-full flex flex-col relative">
    <ToastContainer />

    <!-- STEP 0: Choose creation method -->
    <div v-if="step === 0" class="flex-1 flex flex-col px-6 pb-16">
      <!-- Breadcrumb -->
      <div class="flex items-center gap-2 text-sm text-[#83939C] pt-8 pb-6">
        <NuxtLink to="/dashboard" class="hover:text-[#000000] transition-colors flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5 text-[#FF8E2C] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          {{ t.navCarousels }}
        </NuxtLink>
        <span>/</span>
        <span class="text-[#000000] font-medium">{{ t.navNewCarousel }}</span>
      </div>

      <!-- Center content -->
      <div class="flex-1 flex flex-col items-center justify-center">
      <div class="w-full max-w-2xl flex flex-col items-center gap-6">
        <h1 class="text-2xl font-bold text-[#000000] tracking-tight">{{ t.chooseMethod }}</h1>

        <!-- Pill tabs -->
        <div class="flex items-center gap-2 flex-wrap justify-center">
          <button v-for="type in sourceTypes" :key="type.key"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium border-2 transition-all duration-150 bg-white"
            :class="sourceType === type.key
              ? 'border-[#2B31B3] text-[#2B31B3]'
              : 'border-[#E6E8EA] text-[#4E616B] hover:border-[#83939C]'"
            @click="sourceType = type.key">
            <svg v-if="type.key === 'text'" class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <svg v-else-if="type.key === 'video'" class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <svg v-else-if="type.key === 'links'" class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            {{ type.label }}
          </button>
        </div>

        <!-- Input box -->
        <div class="w-full bg-white rounded-2xl border-2 transition-all duration-150"
          :class="focused ? 'border-[#2B31B3]' : 'border-[#E6E8EA]'">

          <!-- Text input -->
          <textarea v-if="sourceType === 'text'" v-model="sourceText"
            class="w-full px-5 pt-4 pb-3 text-[15px] text-[#000000] placeholder-[#83939C] bg-transparent resize-none focus:outline-none leading-relaxed min-h-[120px]"
            :placeholder="t.srcPlaceholder"
            @focus="focused = true" @blur="focused = false"
            @keydown.meta.enter="canSubmit && handleSubmit()"
            @keydown.ctrl.enter="canSubmit && handleSubmit()" />

          <!-- Video URL input -->
          <div v-else-if="sourceType === 'video'" class="px-5 pt-4 pb-3 space-y-2">
            <input
              :value="videoUrl"
              class="w-full text-[15px] text-[#000000] placeholder-[#83939C] bg-transparent focus:outline-none"
              placeholder="https://youtube.com/watch?v=…"
              @input="videoUrl = ($event.target as HTMLInputElement).value"
              @focus="focused = true" @blur="focused = false"
              @keydown.enter="canSubmit && handleSubmit()" />
            <textarea v-model="videoNotes"
              class="w-full text-[15px] text-[#000000] placeholder-[#83939C] bg-transparent resize-none focus:outline-none leading-relaxed min-h-[80px]"
              placeholder="Ключевые моменты, таймкоды или контекст…"
              @focus="focused = true" @blur="focused = false" />
          </div>

          <!-- Links input -->
          <div v-else-if="sourceType === 'links'" class="px-5 pt-4 pb-3 space-y-2">
            <div v-for="(link, i) in links" :key="i" class="flex items-center gap-2">
              <input v-model="links[i]"
                class="flex-1 text-[15px] text-[#000000] placeholder-[#83939C] bg-transparent focus:outline-none"
                :placeholder="`https://… (ссылка ${i + 1})`"
                @focus="focused = true" @blur="focused = false" />
              <button v-if="links.length > 1" class="text-[#83939C] hover:text-red-500 transition-colors shrink-0"
                @click="links.splice(i, 1)">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <button class="text-xs text-[#2B31B3] font-medium hover:underline" @click="links.push('')">{{ t.srcAddLink }}</button>
          </div>

          <!-- Bottom bar: mic + send -->
          <div class="flex items-center justify-end gap-2 px-3 pb-3">
            <button class="w-8 h-8 rounded-full flex items-center justify-center text-[#83939C] hover:bg-[#F4F5F6] transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 016 0v6a3 3 0 01-3 3z" />
              </svg>
            </button>
            <button
              class="w-8 h-8 rounded-full flex items-center justify-center transition-all duration-150"
              :class="canSubmit ? 'bg-[#2B31B3] text-white hover:bg-[#2228a0]' : 'bg-[#E6E8EA] text-[#83939C] cursor-not-allowed'"
              :disabled="!canSubmit || generating"
              @mousedown.prevent
              @click="handleSubmit">
              <svg v-if="generating" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="w-full p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-800">
          {{ error }}
        </div>
      </div>
      </div>
    </div>

    <!-- STEP 1: Preview after generation -->
    <div v-else-if="step === 1 && carousel" class="flex-1 flex flex-col overflow-hidden">
      <!-- Top bar -->
      <div class="shrink-0 border-b border-[#E6E8EA] bg-white px-4 py-3 flex items-center justify-between gap-2">
        <div class="flex items-center gap-2 text-sm text-[#83939C] min-w-0">
          <NuxtLink to="/dashboard" class="hover:text-[#000000] transition-colors flex items-center gap-1.5 shrink-0">
            <svg class="w-3.5 h-3.5 text-[#FF8E2C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            <span class="hidden sm:inline">{{ t.navCarousels }}</span>
          </NuxtLink>
          <span class="hidden sm:inline">/</span>
          <span class="hidden sm:inline">{{ t.navNewCarousel }}</span>
          <span class="hidden sm:inline">/</span>
          <span class="flex items-center gap-1.5 text-[#000000] font-medium truncate">
            <svg class="w-3.5 h-3.5 text-[#914CFF] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="currentSourceType?.icon ?? ''" />
            </svg>
            <span class="hidden sm:inline">{{ currentSourceType?.label }}</span>
          </span>
        </div>
        <div class="flex items-center gap-2">
          <button class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[#E6E8EA] bg-white text-sm text-[#4E616B] hover:bg-[#F4F5F6] transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
            {{ t.sourceTextBtn }}
          </button>
          <button class="w-8 h-8 rounded-xl flex items-center justify-center text-[#4E616B] hover:bg-[#F4F5F6] transition-colors"
            title="Назад" @click="step = 0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Hint -->
      <div class="shrink-0 bg-white border-b border-[#E6E8EA] px-4 py-3">
        <p v-if="generatingPreview" class="text-sm text-[#83939C] flex items-center gap-2">
          <span class="w-3.5 h-3.5 border-2 border-[#2B31B3]/30 border-t-[#2B31B3] rounded-full animate-spin shrink-0 inline-block" />
          {{ t.generatingSlides }}
        </p>
        <p v-else class="text-sm text-[#83939C]">{{ t.previewHint }}</p>
      </div>

      <!-- Slide preview area -->
      <div class="flex-1 overflow-y-auto">

        <!-- EXPORT MODE: horizontal scrollable list of all slides with per-slide download -->
        <div v-if="exportUrl && slides.length > 0" class="flex gap-4 px-6 py-5 overflow-x-auto">
          <div v-for="(slide, i) in slides" :key="slide.id" class="flex flex-col items-center gap-2 shrink-0">
            <!-- Slide card -->
            <div class="overflow-hidden rounded-2xl border-2 border-[#E6E8EA] shadow-sm"
              style="width: 180px">
              <SlidePreview :slide="slide" :design="design" />
            </div>
            <!-- Download button under each slide -->
            <button
              class="w-full flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#E6E8EA] bg-white text-xs font-medium text-[#3a3a3c] hover:bg-[#F4F5F6] hover:border-[#c6c6c8] transition-all duration-150"
              @click="downloadFile(exportSlideUrls[i], `slide_${String(i + 1).padStart(2, '0')}.png`)">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {{ i + 1 }}
            </button>
          </div>
        </div>

        <!-- EDITOR MODE: prev/next nav + single slide preview -->
        <template v-else>
          <!-- Prev/Next nav + copy/delete -->
          <div class="flex items-center justify-center gap-2 pt-5 pb-3">
            <button class="w-9 h-9 rounded-full border border-[#E6E8EA] bg-white flex items-center justify-center text-[#4E616B] hover:bg-[#F4F5F6] transition-colors disabled:opacity-30"
              :disabled="previewIndex === 0"
              @click="previewIndex--">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <span class="text-sm text-[#83939C] tabular-nums w-12 text-center">{{ previewIndex + 1 }} / {{ slides.length || slidesCount }}</span>
            <button class="w-9 h-9 rounded-full border border-[#E6E8EA] bg-white flex items-center justify-center text-[#4E616B] hover:bg-[#F4F5F6] transition-colors disabled:opacity-30"
              :disabled="previewIndex >= (slides.length || slidesCount) - 1"
              @click="previewIndex++">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <template v-if="editorMode">
              <div class="w-px h-5 bg-[#E6E8EA] mx-1" />

              <!-- Copy slide text -->
              <button class="w-9 h-9 rounded-full border border-[#E6E8EA] bg-white flex items-center justify-center text-[#4E616B] hover:bg-[#F4F5F6] transition-colors disabled:opacity-30"
                title="Копировать текст слайда"
                :disabled="!slides[previewIndex]"
                @click="handleCopySlideText">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </button>

              <!-- Delete current slide -->
              <button class="w-9 h-9 rounded-full border border-[#E6E8EA] bg-white flex items-center justify-center text-[#4E616B] hover:bg-red-50 hover:border-red-200 hover:text-red-500 transition-colors disabled:opacity-30"
                title="Удалить слайд"
                :disabled="!slides[previewIndex] || slides.length <= 1"
                @click="handleDeleteSlide">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </template>
          </div>

          <!-- Loading skeleton -->
          <div v-if="generatingPreview" class="flex items-center justify-center gap-4 px-4 pb-6">
            <div class="hidden sm:block rounded-xl border border-[#E6E8EA] bg-white overflow-hidden shrink-0 flex items-center justify-center opacity-40"
              style="width:160px;height:200px">
              <div class="w-5 h-5 border-2 border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin" />
            </div>
            <div class="rounded-2xl border border-[#E6E8EA] bg-white overflow-hidden shrink-0 flex items-center justify-center w-full sm:w-auto"
              style="max-width:340px;aspect-ratio:4/5">
              <div class="w-6 h-6 border-2 border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin" />
            </div>
            <div class="hidden sm:block rounded-xl border border-[#E6E8EA] bg-white overflow-hidden shrink-0 flex items-center justify-center opacity-40"
              style="width:160px;height:200px">
              <div class="w-5 h-5 border-2 border-[#2B31B3]/20 border-t-[#2B31B3] rounded-full animate-spin" />
            </div>
          </div>

          <!-- Generated slides -->
          <div v-else-if="slides.length > 0" class="flex items-center justify-center gap-4 px-4 pb-6">
            <div v-if="slides[previewIndex - 1]"
              class="hidden sm:block cursor-pointer shrink-0 overflow-hidden rounded-xl border-2 border-[#E6E8EA] opacity-50 hover:opacity-75 transition-all duration-200"
              style="width:140px"
              @click="previewIndex--">
              <SlidePreview :slide="slides[previewIndex - 1]" :design="design" />
            </div>
            <div v-else class="hidden sm:block shrink-0" style="width:140px" />

            <div class="shrink-0 overflow-hidden rounded-2xl border-2 border-[#2B31B3] shadow-[0_0_0_4px_rgba(43,49,179,0.12)] transition-all duration-200"
              style="width:min(320px,calc(100vw - 48px))">
              <SlidePreview
                :slide="showDesignDrawer && slides[previewIndex] ? { ...slides[previewIndex], overrides: undefined } : slides[previewIndex]"
                :design="design" />
            </div>

            <div v-if="slides[previewIndex + 1]"
              class="hidden sm:block cursor-pointer shrink-0 overflow-hidden rounded-xl border-2 border-[#E6E8EA] opacity-50 hover:opacity-75 transition-all duration-200"
              style="width:140px"
              @click="previewIndex++">
              <SlidePreview :slide="slides[previewIndex + 1]" :design="design" />
            </div>
            <div v-else class="hidden sm:block shrink-0" style="width:140px" />
          </div>
        </template>
      </div>

      <!-- Шаблон modal: centered slide-up with backdrop -->
      <Transition
        enter-active-class="transition-all duration-250 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0">
        <div v-if="showDesignDrawer && carousel && editorMode"
          class="absolute inset-0 z-[60] flex flex-col"
          @click.self="cancelDesignDrawer">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/30" @click="cancelDesignDrawer" />
          <!-- Modal panel slides up from bottom, centered -->
          <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-full max-w-lg bg-white rounded-t-2xl shadow-2xl flex flex-col"
            style="max-height: 70dvh"
            @click.stop>
            <!-- drag handle -->
            <div class="shrink-0 flex justify-center pt-3 pb-1">
              <div class="w-10 h-1 rounded-full bg-[#E6E8EA]" />
            </div>
            <!-- Modal header -->
            <div class="flex items-center justify-between px-5 py-2.5 border-b border-[#F2F2F7] shrink-0">
              <span class="text-sm font-semibold text-[#000000]">{{ designPanelTabs.find(t => t.tab === activeDesignTab)?.label }}</span>
              <button class="w-7 h-7 rounded-full flex items-center justify-center text-[#83939C] hover:bg-[#F4F5F6] transition-colors"
                @click="cancelDesignDrawer">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <!-- DesignPanel scoped to the active tab -->
            <div class="flex-1 overflow-y-auto">
              <DesignPanel v-model="design" :initial-tab="activeDesignTab" :hide-tab-bar="true"
                :active-slide="slides[previewIndex] ?? null"
                @apply-to-all="saveDesign" @update:slide-overrides="onSlideOverrides" @cancel="cancelDesignDrawer" />
            </div>
          </div>
        </div>
      </Transition>

      <!-- Bottom toolbar: preview mode -->
      <div v-if="!editorMode" class="shrink-0 px-3 pb-3 pt-2 flex items-center justify-center gap-2 flex-wrap">
        <!-- Floating pill container -->
        <div class="flex items-center gap-1.5 bg-white rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.10)] border border-[#E6E8EA] px-2 py-1.5 flex-wrap justify-center">

          <!-- Slides count picker -->
          <div class="relative">
            <button class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-sm text-[#4E616B] hover:bg-[#F4F5F6] transition-colors"
              @click.stop="showSlidesMenu = !showSlidesMenu; showLangMenu = false">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
              {{ slides.length || slidesCount }} слайдов
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-if="showSlidesMenu"
              class="absolute bottom-full mb-1 left-0 bg-white border border-[#E6E8EA] rounded-xl shadow-lg z-10 py-1 min-w-[120px]">
              <button v-for="n in [6,7,8,9,10]" :key="n"
                class="w-full text-left px-3 py-1.5 text-sm transition-colors"
                :class="slidesCount === n ? 'text-[#2B31B3] font-semibold bg-[#EEF0FF]' : 'text-[#4E616B] hover:bg-[#F4F5F6]'"
                @click.stop="slidesCount = n; showSlidesMenu = false">
                {{ n }} слайдов
              </button>
            </div>
          </div>

          <div class="w-px h-4 bg-[#E6E8EA]" />

          <!-- Language picker -->
          <div class="relative">
            <button class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-sm text-[#4E616B] hover:bg-[#F4F5F6] transition-colors"
              @click.stop="showLangMenu = !showLangMenu; showSlidesMenu = false">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
              </svg>
              {{ currentLang?.label }}
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-if="showLangMenu"
              class="absolute bottom-full mb-1 left-0 bg-white border border-[#E6E8EA] rounded-xl shadow-lg z-10 py-1 min-w-[140px]">
              <button v-for="lang in languages" :key="lang.code"
                class="w-full text-left px-3 py-1.5 text-sm transition-colors"
                :class="language === lang.code ? 'text-[#2B31B3] font-semibold bg-[#EEF0FF]' : 'text-[#4E616B] hover:bg-[#F4F5F6]'"
                @click.stop="language = lang.code; showLangMenu = false">
                {{ lang.label }}
              </button>
            </div>
          </div>

          <div class="w-px h-4 bg-[#E6E8EA]" />

          <!-- Template quick picker -->
          <button class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-sm text-[#4E616B] hover:bg-[#F4F5F6] transition-colors"
            @click="openDesignDrawer('template'); editorMode = true">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
            </svg>
            {{ t.tabTemplate }}
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <div class="w-px h-4 bg-[#E6E8EA]" />

          <!-- Redo -->
          <button class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-sm text-[#914CFF] hover:bg-[#F3E8FF] transition-colors"
            :disabled="generatingPreview" @click="handleRegenerate">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ t.redoBtn }}
          </button>
        </div>

        <!-- In editor (separate pill, prominent) -->
        <button
          class="flex items-center gap-2 px-5 py-2.5 rounded-2xl text-sm font-semibold shadow-[0_4px_20px_rgba(43,49,179,0.25)] transition-all"
          :class="generatingPreview ? 'bg-[#E6E8EA] text-[#83939C] cursor-not-allowed shadow-none' : 'bg-[#2B31B3] text-white hover:bg-[#2228a0]'"
          :disabled="generatingPreview"
          @click="editorMode = true">
          {{ t.toEditorBtn }}
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Bottom toolbar: editor mode -->
      <div v-else class="shrink-0 pb-3 pt-2 px-3 flex justify-center">

        <!-- Toolbar pill (export success or normal) -->
        <div class="inline-flex items-center gap-0.5 bg-white rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.10)] border border-[#E6E8EA] px-1.5 py-1.5 max-w-full overflow-x-auto">

          <!-- Export success content -->
          <template v-if="exportUrl">
            <!-- Success check + text -->
            <div class="flex items-center gap-1.5 px-2.5 py-1.5 shrink-0">
              <svg class="w-4 h-4 text-[#16a34a] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-sm font-medium text-[#3a3a3c] whitespace-nowrap">Все {{ slides.length }} слайдов готовы</span>
            </div>

            <div class="w-px h-8 bg-[#E6E8EA] shrink-0 mx-1" />

            <!-- Download all -->
            <button
              class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-semibold bg-[#2B31B3] text-white hover:bg-[#2228a0] transition-colors shrink-0"
              @click="downloadFile(exportUrl ?? undefined, 'slides.zip')">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Скачать все
            </button>

            <div class="w-px h-8 bg-[#E6E8EA] shrink-0 mx-0.5" />

            <!-- Back to editor -->
            <button
              class="flex flex-col items-center gap-0.5 px-2.5 py-1.5 rounded-xl transition-colors shrink-0 text-[#4E616B] hover:bg-[#F4F5F6]"
              @click="exportUrl = null">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 19l-7-7 7-7" />
              </svg>
              <span class="text-[10px] leading-none font-medium">Назад</span>
            </button>
          </template>

          <!-- Normal editor toolbar -->
          <template v-else>
            <button v-for="dp in designPanelTabs" :key="dp.tab"
              class="flex flex-col items-center gap-0.5 px-2.5 py-1.5 rounded-xl transition-colors shrink-0"
              :class="activeDesignTab === dp.tab && showDesignDrawer
                ? 'bg-[#EEF0FF] text-[#2B31B3]'
                : 'text-[#4E616B] hover:bg-[#F4F5F6]'"
              @click="openDesignDrawer(dp.tab)">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="dp.icon" />
              </svg>
              <span class="text-[10px] leading-none font-medium">{{ dp.label }}</span>
            </button>

            <div class="w-px h-8 bg-[#E6E8EA] shrink-0 mx-1" />

            <button
              class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-semibold bg-[#2B31B3] text-white hover:bg-[#2228a0] transition-colors shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="exporting || !carousel || generatingPreview"
              @click="handleExport">
              <svg v-if="exporting" class="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {{ exporting ? exportStatus : t.exportBtn }}
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>


</template>

<script setup lang="ts">
import type { Carousel, CarouselDesign, Slide } from "~/types"

definePageMeta({ layout: 'default', ssr: false })

const config = useRuntimeConfig()
const route = useRoute()
const { createCarousel } = useCarousels()
const { startGeneration, watchGeneration } = useGeneration()
const { getLatestExport, startExport, pollExport } = useExport()
const { authHeaders } = useAuth()
const { t } = useLang()

// Design state (mirrors edit page defaults)
const design = ref<CarouselDesign>({
  template: "minimal",
  bg_color: "#f8f8f6",
  bg_image_url: null,
  darkening: 0,
  pattern: "none",
  pattern_color: "#000000",
  pattern_opacity: 0.06,
  title_font: "system",
  body_font: "system",
  accent_color: null,
  title_highlight: null,
  align_h: "left",
  align_v: "center",
  aspect_ratio: "4:5",
  padding: 40,
  show_header: false,
  header_text: "",
  show_footer: false,
  footer_text: "",
})

// Design drawer
const showDesignDrawer = ref(false)
const activeDesignTab = ref("template")

const designPanelTabs = computed(() => [
  { tab: "template",    label: t.value.tabTemplate,    icon: "M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" },
  { tab: "background",  label: t.value.tabBackground,  icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" },
  { tab: "typography",  label: t.value.tabTypography,  icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" },
  { tab: "layout",      label: t.value.tabLayout,      icon: "M4 6h16M4 12h16M4 18h7" },
  { tab: "extra",       label: t.value.tabExtra,       icon: "M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" },
])

let designSnapshot: CarouselDesign | null = null

const openDesignDrawer = (tab: string) => {
  if (showDesignDrawer.value && activeDesignTab.value === tab) {
    showDesignDrawer.value = false
  } else {
    designSnapshot = { ...design.value }
    activeDesignTab.value = tab
    showDesignDrawer.value = true
  }
}

const cancelDesignDrawer = () => {
  if (designSnapshot) design.value = { ...designSnapshot }
  showDesignDrawer.value = false
}

const persistDesign = async (d: CarouselDesign) => {
  if (!carousel.value) return
  try {
    await $fetch(`${config.public.apiBase}/carousels/${carousel.value.id}/design`, {
      method: "PATCH",
      headers: authHeaders(),
      body: d,
    })
  } catch {}
}

// Watch design changes and auto-save (debounced) — only persists, never reassigns design
let saveTimer: ReturnType<typeof setTimeout> | null = null
watch(design, (d) => {
  if (!carousel.value) return
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(() => persistDesign({ ...d }), 800)
}, { deep: true })

const saveDesign = (d: CarouselDesign) => {
  design.value = { ...d }
  showDesignDrawer.value = false
}

const onSlideOverrides = async (ov: import("~/types").SlideOverrides) => {
  const slide = slides.value[previewIndex.value]
  if (!slide || !carousel.value) return
  // Save override on current slide
  slides.value[previewIndex.value] = { ...slide, overrides: ov }
  // Revert global design back to snapshot so other slides are unaffected
  if (designSnapshot) design.value = { ...designSnapshot }
  showDesignDrawer.value = false
  try {
    await $fetch(`${config.public.apiBase}/carousels/${carousel.value.id}/slides/${slide.id}`, {
      method: "PATCH",
      headers: authHeaders(),
      body: { overrides: ov },
    })
  } catch {}
}

// Step 0 state
const step = ref(0)
const sourceType = ref("text")
const sourceText = ref("")
const videoUrl = ref("")
const videoNotes = ref("")
const links = ref<string[]>([""])
const slidesCount = ref(8)
const language = ref("ru")
const focused = ref(false)
const generating = ref(false)
const error = ref("")
const showSlidesMenu = ref(false)
const showLangMenu = ref(false)

// Editor mode (toggled by "В редактор" button)
const editorMode = ref(false)

// Step 1 state
const carousel = ref<Carousel | null>(null)
const slides = ref<Slide[]>([])
const generatingPreview = ref(false)
const previewIndex = ref(0)
const exporting = ref(false)
const exportStatus = ref("Queuing…")
const exportUrl = ref<string | null>(null)
const exportSlideUrls = ref<string[]>([])

const sourceTypes = computed(() => [
  { key: "text",  label: t.value.srcText,  icon: "M4 6h16M4 12h8m-8 6h16" },
  { key: "video", label: t.value.srcVideo, icon: "M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" },
  { key: "links", label: t.value.srcLinks, icon: "M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" },
])

const currentSourceType = computed(() => sourceTypes.value.find((t) => t.key === sourceType.value))

const languages = [
  { code: "ru", label: "🇷🇺 Русский" },
  { code: "en", label: "🇬🇧 English" },
  { code: "fr", label: "🇫🇷 Français" },
]

const currentLang = computed(() => languages.find((l) => l.code === language.value))

const canSubmit = computed(() => {
  if (sourceType.value === "text")  return sourceText.value.trim().length > 10
  if (sourceType.value === "video") return videoUrl.value.trim().length > 5
  if (sourceType.value === "links") return links.value.some((l) => l.trim())
  return false
})

const deriveTitle = () => {
  if (sourceType.value === "text") {
    const first = sourceText.value.trim().split(/\n/)[0].slice(0, 80)
    return first || "Новая карусель"
  }
  if (sourceType.value === "video") return videoUrl.value.slice(0, 60) || "Новая карусель"
  return "Новая карусель"
}

const buildSourcePayload = () => {
  if (sourceType.value === "text")  return { text: sourceText.value }
  if (sourceType.value === "video") return { video_url: videoUrl.value, notes: videoNotes.value }
  if (sourceType.value === "links") return { links: links.value.filter(Boolean), notes: sourceText.value }
  return {}
}

const loadSlides = async (carouselId: string) => {
  try {
    const data = await $fetch<Slide[]>(`${config.public.apiBase}/carousels/${carouselId}/slides`, {
      headers: authHeaders(),
    })
    slides.value = data
  } catch {}
}

const handleSubmit = async () => {
  if (!canSubmit.value || generating.value) return
  error.value = ""
  generating.value = true
  try {
    const created = await createCarousel({
      title: deriveTitle(),
      source_type: sourceType.value,
      source_payload: buildSourcePayload(),
      format: { slides_count: slidesCount.value, language: language.value as any },
    })
    carousel.value = created
    step.value = 1
    generatingPreview.value = true
    generating.value = false

    const gen = await startGeneration(created.id)
    watchGeneration(
      gen.id,
      async () => {
        generatingPreview.value = false
        await loadSlides(created.id)
      },
      () => {
        generatingPreview.value = false
        error.value = t.value.generationFailed
        step.value = 0
      },
    )
  } catch (e: any) {
    error.value = e?.data?.detail || "Что-то пошло не так. Попробуйте снова."
    step.value = 0
    generating.value = false
    generatingPreview.value = false
  }
}

const handleRegenerate = async () => {
  if (!carousel.value || generatingPreview.value) return
  generatingPreview.value = true
  slides.value = []
  previewIndex.value = 0
  try {
    // Patch format (language + slides count) before regenerating
    await $fetch(`${config.public.apiBase}/carousels/${carousel.value.id}`, {
      method: "PATCH",
      headers: authHeaders(),
      body: { format: { slides_count: slidesCount.value, language: language.value } },
    })
    const gen = await startGeneration(carousel.value.id)
    watchGeneration(
      gen.id,
      async () => {
        generatingPreview.value = false
        await loadSlides(carousel.value!.id)
      },
      () => { generatingPreview.value = false },
    )
  } catch { generatingPreview.value = false }
}

const copyFeedback = ref(false)
const handleCopySlideText = async () => {
  const slide = slides.value[previewIndex.value]
  if (!slide) return
  const text = [slide.title, slide.body, slide.footer_cta].filter(Boolean).join('\n\n')
  try {
    await navigator.clipboard.writeText(text)
    copyFeedback.value = true
    setTimeout(() => { copyFeedback.value = false }, 1500)
  } catch {}
}

const handleDeleteSlide = async () => {
  const slide = slides.value[previewIndex.value]
  if (!slide || !carousel.value || slides.value.length <= 1) return
  try {
    await $fetch(`${config.public.apiBase}/carousels/${carousel.value.id}/slides/${slide.id}`, {
      method: "DELETE",
      headers: authHeaders(),
    })
    slides.value.splice(previewIndex.value, 1)
    if (previewIndex.value >= slides.value.length) previewIndex.value = slides.value.length - 1
  } catch {}
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

const handleExport = async () => {
  if (!carousel.value || exporting.value) return

  exporting.value = true
  exportStatus.value = "Queuing…"
  try {
    // Flush any pending design save before starting export
    if (saveTimer) { clearTimeout(saveTimer); saveTimer = null }
    await persistDesign({ ...design.value })

    const exp = await startExport(carousel.value.id)
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

const loadCarouselById = async (id: string) => {
  console.log('[new.vue] loadCarouselById', id)
  try {
    const [loadedCarousel, loadedSlides] = await Promise.all([
      $fetch<Carousel>(`${config.public.apiBase}/carousels/${id}`, { headers: authHeaders() }),
      $fetch<Slide[]>(`${config.public.apiBase}/carousels/${id}/slides`, { headers: authHeaders() }),
    ])
    console.log('[new.vue] fetched ok, slides:', loadedSlides.length, 'setting step=1')
    carousel.value = loadedCarousel
    slides.value = loadedSlides
    if (loadedCarousel.design) design.value = { ...loadedCarousel.design }
    await nextTick()
    step.value = 1
    editorMode.value = true
    // Auto-restore last export if available
    const latest = await getLatestExport(id)
    if (latest?.file_url) {
      exportUrl.value = latest.file_url
      exportSlideUrls.value = latest.slide_urls ?? []
    }
  } catch (e) {
    console.error('[new.vue] load failed:', e)
  }
}

// React to ?id= on both initial load and when the component is reused (same route, new query)
watch(
  () => route.query.id as string | undefined,
  (id) => {
    console.log('[new.vue] watch id=', id, 'route.query=', JSON.stringify(route.query))
    if (id) loadCarouselById(id)
  },
  { immediate: true },
)

// Close dropdowns on outside click
onMounted(() => {
  document.addEventListener('click', () => {
    showSlidesMenu.value = false
    showLangMenu.value = false
  })

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (step.value !== 1) return
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
    if (e.key === 'ArrowLeft' && previewIndex.value > 0) previewIndex.value--
    if (e.key === 'ArrowRight' && previewIndex.value < slides.value.length - 1) previewIndex.value++
  })
})
</script>
