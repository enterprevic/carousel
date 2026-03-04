<template>
  <div class="flex flex-col h-full">
    <!-- Tabs -->
    <div class="shrink-0 px-3 pt-3 pb-0">
      <div class="flex gap-0.5 bg-[#f2f2f7] rounded-xl p-1">
        <button v-for="tab in tabs" :key="tab.key"
          class="flex-1 flex flex-col items-center gap-0.5 py-1.5 px-1 rounded-lg text-[10px] font-medium transition-all duration-150 leading-tight"
          :class="activeTab === tab.key
            ? 'bg-white text-[#0071e3] shadow-sm'
            : 'text-[#6c6c70] hover:text-[#3a3a3c]'"
          @click="activeTab = tab.key">
          <component :is="'svg'" class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="tab.icon" />
          </component>
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-5">

      <!-- Template -->
      <template v-if="activeTab === 'template'">
        <div>
          <label class="label">Template</label>
          <div class="grid grid-cols-2 gap-2">
            <button v-for="t in templates" :key="t.key"
              class="rounded-xl overflow-hidden border-2 transition-all duration-150"
              :class="localDesign.template === t.key
                ? 'border-[#0071e3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7]'"
              @click="setTemplate(t.key)">
              <div class="h-16 flex flex-col justify-center gap-1 px-2.5" :style="{ background: t.bg, fontFamily: t.font }">
                <div class="font-bold leading-none truncate" :style="{ color: t.title, fontSize: '7px' }">TITLE TEXT</div>
                <div class="leading-none truncate" :style="{ color: t.body, fontSize: '5.5px' }">Body content here</div>
                <div class="font-semibold leading-none truncate" :style="{ color: t.accent, fontSize: '5px' }">Call to action</div>
              </div>
              <div class="py-1.5 text-center text-[10px] font-semibold text-[#3a3a3c] bg-white">
                {{ t.label }}
              </div>
            </button>
          </div>
        </div>

        <!-- Per-slide style overrides -->
        <div v-if="activeSlide" class="border-t border-[#f2f2f7] pt-1">
          <div class="flex items-center justify-between mb-3">
            <label class="label mb-0">This Slide Only</label>
            <button v-if="slideOv.template || slideOv.accent_color || slideOv.title_highlight || slideOv.align_h || slideOv.align_v"
              class="text-[11px] text-[#ff3b30] font-semibold hover:underline"
              @click="setSlideOv({ template: null, accent_color: null, title_highlight: null, align_h: null, align_v: null })">
              Reset
            </button>
          </div>

          <!-- Template override -->
          <div class="mb-4">
            <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">Template</label>
            <div class="grid grid-cols-2 gap-1.5">
              <button v-for="t in templates" :key="t.key"
                class="rounded-xl overflow-hidden border-2 transition-all duration-150"
                :class="slideOv.template === t.key
                  ? 'border-[#0071e3] shadow-[0_0_0_3px_rgba(0,113,227,0.12)]'
                  : 'border-[#e5e5ea] hover:border-[#d2d2d7]'"
                @click="setSlideOv({ template: slideOv.template === t.key ? null : t.key as any })">
                <div class="h-10 flex flex-col justify-center gap-0.5 px-2" :style="{ background: t.bg, fontFamily: t.font }">
                  <div class="font-bold leading-none truncate" :style="{ color: t.title, fontSize: '6px' }">TITLE</div>
                  <div class="leading-none truncate" :style="{ color: t.body, fontSize: '5px' }">Body text</div>
                </div>
                <div class="py-1 text-center text-[9px] font-semibold text-[#3a3a3c] bg-white">{{ t.label }}</div>
              </button>
            </div>
          </div>

          <!-- Accent color override -->
          <div class="mb-3">
            <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">Accent Color</label>
            <div class="flex items-center gap-2">
              <div class="relative shrink-0">
                <div class="w-8 h-8 rounded-xl border border-[#c6c6c8] overflow-hidden cursor-pointer shadow-sm">
                  <input type="color" :value="slideOv.accent_color || '#0071e3'"
                    class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                    @input="setSlideOv({ accent_color: ($event.target as HTMLInputElement).value })" />
                  <div class="w-full h-full" :style="{ backgroundColor: slideOv.accent_color || localDesign.accent_color || '#0071e3' }" />
                </div>
              </div>
              <input :value="slideOv.accent_color || ''" class="input font-mono text-sm flex-1"
                placeholder="Global default"
                @input="setSlideOv({ accent_color: ($event.target as HTMLInputElement).value || null })" />
              <button v-if="slideOv.accent_color" class="text-[11px] text-[#ff3b30] font-semibold shrink-0"
                @click="setSlideOv({ accent_color: null })">✕</button>
            </div>
          </div>

          <!-- Title highlight override -->
          <div class="mb-3">
            <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">Title Highlight</label>
            <div class="flex items-center gap-2">
              <div class="relative shrink-0">
                <div class="w-8 h-8 rounded-xl border border-[#c6c6c8] overflow-hidden cursor-pointer shadow-sm">
                  <input type="color" :value="slideOv.title_highlight || '#ffff00'"
                    class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                    @input="setSlideOv({ title_highlight: ($event.target as HTMLInputElement).value })" />
                  <div class="w-full h-full" :style="{
                    backgroundColor: slideOv.title_highlight || 'transparent',
                    backgroundImage: slideOv.title_highlight ? 'none' : 'repeating-linear-gradient(45deg,#d1d1d6 0,#d1d1d6 1px,transparent 0,transparent 50%)',
                    backgroundSize: '4px 4px'
                  }" />
                </div>
              </div>
              <input :value="slideOv.title_highlight || ''" class="input font-mono text-sm flex-1"
                placeholder="None"
                @input="setSlideOv({ title_highlight: ($event.target as HTMLInputElement).value || null })" />
              <button v-if="slideOv.title_highlight" class="text-[11px] text-[#ff3b30] font-semibold shrink-0"
                @click="setSlideOv({ title_highlight: null })">✕</button>
            </div>
          </div>

          <!-- Alignment overrides -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">H-Align</label>
              <div class="flex gap-1">
                <button v-for="a in ['left','center','right']" :key="a"
                  class="flex-1 py-1.5 rounded-lg border transition-all duration-150"
                  :class="slideOv.align_h === a ? 'border-[#0071e3] bg-[#0071e3] text-white' : 'border-[#e5e5ea] bg-white text-[#3a3a3c] hover:border-[#c6c6c8]'"
                  @click="setSlideOv({ align_h: slideOv.align_h === a ? null : a as any })">
                  <svg class="w-3.5 h-3.5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="a === 'left'"   stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M3 12h12M3 18h8" />
                    <path v-if="a === 'center'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M6 12h12M7 18h10" />
                    <path v-if="a === 'right'"  stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M9 12h12M13 18h8" />
                  </svg>
                </button>
              </div>
            </div>
            <div>
              <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">V-Align</label>
              <div class="flex gap-1">
                <button v-for="a in ['top','center','bottom']" :key="a"
                  class="flex-1 py-1.5 rounded-lg border text-[9px] font-medium capitalize transition-all duration-150"
                  :class="slideOv.align_v === a ? 'border-[#0071e3] bg-[#0071e3] text-white' : 'border-[#e5e5ea] bg-white text-[#3a3a3c] hover:border-[#c6c6c8]'"
                  @click="setSlideOv({ align_v: slideOv.align_v === a ? null : a as any })">
                  {{ a[0] }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Background -->
      <template v-if="activeTab === 'background'">
        <!-- Pattern selector -->
        <div>
          <label class="label">Background Pattern</label>
          <div class="grid grid-cols-4 gap-1.5">
            <button v-for="p in patternOptions" :key="p.key"
              class="flex flex-col items-center gap-1 py-2 rounded-xl border-2 transition-all duration-150"
              :class="(localDesign.pattern ?? 'none') === p.key
                ? 'border-[#0071e3] bg-[#0071e3]/5'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.pattern = p.key">
              <svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"
                :style="(localDesign.pattern ?? 'none') === p.key ? 'color:#0071e3' : 'color:#8e8e93'">
                <path :d="p.svgPath" :fill="p.filled ? 'currentColor' : 'none'"
                  :stroke="p.filled ? 'none' : 'currentColor'" stroke-width="1.2" />
              </svg>
              <span class="text-[9px] font-medium"
                :style="(localDesign.pattern ?? 'none') === p.key ? 'color:#0071e3' : 'color:#6c6c70'">{{ p.label }}</span>
            </button>
          </div>
        </div>

        <div v-if="localDesign.pattern && localDesign.pattern !== 'none'" class="space-y-4">
          <div>
            <label class="label">Pattern Color</label>
            <div class="flex items-center gap-2.5">
              <ColorSwatch v-model="localDesign.pattern_color" />
              <input v-model="localDesign.pattern_color" class="input font-mono text-sm" placeholder="#000000" />
            </div>
          </div>
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="label mb-0">Opacity</label>
              <span class="text-xs text-[#0071e3] font-semibold">{{ Math.round((localDesign.pattern_opacity ?? 0.06) * 100) }}%</span>
            </div>
            <input type="range" v-model.number="localDesign.pattern_opacity" min="0.01" max="0.5" step="0.01" />
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <!-- Solid bg color -->
        <div>
          <label class="label">Background Color</label>
          <div class="flex items-center gap-2.5">
            <ColorSwatch v-model="localDesign.bg_color" />
            <input v-model="localDesign.bg_color" class="input font-mono text-sm" placeholder="#ffffff" />
          </div>
        </div>

        <!-- Image -->
        <div>
          <label class="label">Background Image</label>
          <input type="file" accept="image/*" ref="fileInput" class="hidden" @change="handleImageUpload" />
          <button class="btn-secondary w-full text-sm" :disabled="uploading" @click="(fileInput as HTMLInputElement)?.click()">
            <svg v-if="uploading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ uploading ? 'Uploading…' : 'Upload Image' }}
          </button>
          <div v-if="localDesign.bg_image_url" class="mt-2 flex items-center gap-2.5">
            <img :src="localDesign.bg_image_url" class="w-12 h-12 object-cover rounded-xl border border-[#e5e5ea]" />
            <button class="text-xs text-[#ff3b30] font-medium hover:underline"
              @click="localDesign.bg_image_url = null">Remove</button>
          </div>
        </div>

        <div v-if="localDesign.bg_image_url">
          <div class="flex items-center justify-between mb-2">
            <label class="label mb-0">Darkening</label>
            <span class="text-xs text-[#0071e3] font-semibold">{{ Math.round(localDesign.darkening * 100) }}%</span>
          </div>
          <input type="range" v-model.number="localDesign.darkening" min="0" max="0.9" step="0.05" />
        </div>

        <!-- Per-slide pattern override -->
        <div v-if="activeSlide" class="border-t border-[#f2f2f7] pt-1">
          <div class="flex items-center justify-between mb-3">
            <label class="label mb-0">This Slide Only</label>
            <button v-if="slideOv.pattern || slideOv.pattern_color || slideOv.pattern_opacity != null"
              class="text-[11px] text-[#ff3b30] font-semibold hover:underline"
              @click="setSlideOv({ pattern: null, pattern_color: null, pattern_opacity: null })">
              Reset
            </button>
          </div>
          <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">Pattern</label>
          <div class="grid grid-cols-4 gap-1.5">
            <button v-for="p in patternOptions" :key="p.key"
              class="flex flex-col items-center gap-1 py-2 rounded-xl border-2 transition-all duration-150"
              :class="(slideOv.pattern ?? null) === p.key
                ? 'border-[#0071e3] bg-[#0071e3]/5'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="setSlideOv({ pattern: (slideOv.pattern === p.key ? null : p.key) as any })">
              <svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"
                :style="(slideOv.pattern ?? null) === p.key ? 'color:#0071e3' : 'color:#8e8e93'">
                <path :d="p.svgPath" :fill="p.filled ? 'currentColor' : 'none'"
                  :stroke="p.filled ? 'none' : 'currentColor'" stroke-width="1.2" />
              </svg>
              <span class="text-[9px] font-medium"
                :style="(slideOv.pattern ?? null) === p.key ? 'color:#0071e3' : 'color:#6c6c70'">{{ p.label }}</span>
            </button>
          </div>
          <div v-if="slideOv.pattern && slideOv.pattern !== 'none'" class="mt-3 space-y-3">
            <div>
              <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold mb-1.5 block">Color</label>
              <div class="flex items-center gap-2">
                <div class="relative shrink-0">
                  <div class="w-8 h-8 rounded-xl border border-[#c6c6c8] overflow-hidden cursor-pointer shadow-sm">
                    <input type="color" :value="slideOv.pattern_color || '#000000'"
                      class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                      @input="setSlideOv({ pattern_color: ($event.target as HTMLInputElement).value })" />
                    <div class="w-full h-full" :style="{ backgroundColor: slideOv.pattern_color || '#000000' }" />
                  </div>
                </div>
                <input :value="slideOv.pattern_color || ''" class="input font-mono text-sm flex-1"
                  placeholder="#000000"
                  @input="setSlideOv({ pattern_color: ($event.target as HTMLInputElement).value || null })" />
              </div>
            </div>
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold">Opacity</label>
                <span class="text-xs text-[#0071e3] font-semibold">{{ Math.round((slideOv.pattern_opacity ?? 0.06) * 100) }}%</span>
              </div>
              <input type="range" :value="slideOv.pattern_opacity ?? 0.06" min="0.01" max="0.5" step="0.01"
                @input="setSlideOv({ pattern_opacity: parseFloat(($event.target as HTMLInputElement).value) })" />
            </div>
          </div>
        </div>
      </template>

      <!-- Typography -->
      <template v-if="activeTab === 'typography'">
        <div>
          <label class="label">Title Font</label>
          <div class="grid grid-cols-2 gap-1.5">
            <button v-for="f in fontOptions" :key="f.key"
              class="rounded-xl border-2 py-2 px-2 text-left transition-all duration-150"
              :class="(localDesign.title_font ?? 'system') === f.key
                ? 'border-[#0071e3] bg-[#0071e3]/5 shadow-sm'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.title_font = f.key">
              <div class="text-base font-bold leading-none mb-0.5 text-[#1c1c1e]"
                :style="{ fontFamily: FONT_FAMILIES[f.key] }">
                {{ f.sample }}
              </div>
              <div class="text-[10px] text-[#6c6c70] truncate">{{ f.label }}</div>
            </button>
          </div>
        </div>

        <div>
          <label class="label">Body Font</label>
          <div class="grid grid-cols-2 gap-1.5">
            <button v-for="f in fontOptions" :key="f.key"
              class="rounded-xl border-2 py-2 px-2 text-left transition-all duration-150"
              :class="(localDesign.body_font ?? 'system') === f.key
                ? 'border-[#0071e3] bg-[#0071e3]/5 shadow-sm'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.body_font = f.key">
              <div class="text-base leading-none mb-0.5 text-[#1c1c1e]"
                :style="{ fontFamily: FONT_FAMILIES[f.key] }">
                {{ f.sample }}
              </div>
              <div class="text-[10px] text-[#6c6c70] truncate">{{ f.label }}</div>
            </button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <div>
          <label class="label">Accent Color</label>
          <p class="text-[11px] text-[#6c6c70] mb-2 -mt-1">Used for CTA text. Overrides the template default.</p>
          <div class="flex items-center gap-2.5">
            <ColorSwatch
              :value="localDesign.accent_color || '#0071e3'"
              @input="localDesign.accent_color = ($event.target as HTMLInputElement).value" />
            <input :value="localDesign.accent_color || ''"
              class="input font-mono text-sm" placeholder="Template default"
              @input="localDesign.accent_color = ($event.target as HTMLInputElement).value || null" />
            <button v-if="localDesign.accent_color"
              class="text-xs text-[#ff3b30] font-medium whitespace-nowrap"
              @click="localDesign.accent_color = null">Reset</button>
          </div>
        </div>

        <div>
          <label class="label">Title Highlight</label>
          <p class="text-[11px] text-[#6c6c70] mb-2 -mt-1">Marker-style background behind the title text.</p>
          <div class="flex items-center gap-2.5">
            <ColorSwatch
              :value="localDesign.title_highlight || '#ffff00'"
              @input="localDesign.title_highlight = ($event.target as HTMLInputElement).value" />
            <input :value="localDesign.title_highlight || ''"
              class="input font-mono text-sm" placeholder="No highlight"
              @input="localDesign.title_highlight = ($event.target as HTMLInputElement).value || null" />
            <button v-if="localDesign.title_highlight"
              class="text-xs text-[#ff3b30] font-medium whitespace-nowrap"
              @click="localDesign.title_highlight = null">Remove</button>
          </div>
        </div>
      </template>

      <!-- Layout -->
      <template v-if="activeTab === 'layout'">
        <!-- Image size -->
        <div>
          <label class="label">Image Size</label>
          <div class="flex flex-col gap-2">
            <button v-for="s in sizeOptions" :key="s.key"
              class="flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all duration-150 text-left"
              :class="(localDesign.aspect_ratio ?? '4:5') === s.key
                ? 'border-[#0071e3] bg-[#0071e3]/5 shadow-sm'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.aspect_ratio = s.key">
              <div class="shrink-0 flex items-center justify-center w-8"
                :class="(localDesign.aspect_ratio ?? '4:5') === s.key ? 'text-[#0071e3]' : 'text-[#8e8e93]'">
                <div class="border-2 rounded"
                  :class="(localDesign.aspect_ratio ?? '4:5') === s.key ? 'border-[#0071e3]' : 'border-[#c6c6c8]'"
                  :style="s.key === '4:5'  ? 'width:16px;height:20px' :
                          s.key === '9:16' ? 'width:12px;height:20px' :
                                             'width:20px;height:20px'" />
              </div>
              <div>
                <div class="text-sm font-semibold text-[#1c1c1e]">{{ s.label }}</div>
                <div class="text-xs text-[#6c6c70]">{{ s.sub }}</div>
              </div>
            </button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="label mb-0">Content Padding</label>
            <span class="text-xs text-[#0071e3] font-semibold">{{ localDesign.padding }}px</span>
          </div>
          <input type="range" v-model.number="localDesign.padding" min="20" max="80" step="4" />
        </div>

        <div>
          <label class="label">Horizontal Alignment</label>
          <div class="flex gap-1.5">
            <button v-for="a in ['left','center','right']" :key="a"
              class="flex-1 py-2 text-xs rounded-xl border transition-all duration-150"
              :class="localDesign.align_h === a
                ? 'bg-[#0071e3] text-white border-[#0071e3]'
                : 'bg-white text-[#3a3a3c] border-[#c6c6c8] hover:border-[#8e8e93]'"
              @click="localDesign.align_h = a as any">
              <svg class="w-4 h-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="a === 'left'"   stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M3 12h12M3 18h8" />
                <path v-if="a === 'center'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M6 12h12M7 18h10" />
                <path v-if="a === 'right'"  stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M9 12h12M13 18h8" />
              </svg>
            </button>
          </div>
        </div>

        <div>
          <label class="label">Vertical Alignment</label>
          <div class="flex gap-1.5">
            <button v-for="a in ['top','center','bottom']" :key="a"
              class="flex-1 py-2 text-xs rounded-xl border capitalize transition-all duration-150"
              :class="localDesign.align_v === a
                ? 'bg-[#0071e3] text-white border-[#0071e3]'
                : 'bg-white text-[#3a3a3c] border-[#c6c6c8] hover:border-[#8e8e93]'"
              @click="localDesign.align_v = a as any">
              {{ a }}
            </button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <!-- Header / Footer -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-[#1c1c1e]">Header</span>
            <Toggle v-model="localDesign.show_header" />
          </div>
          <input v-if="localDesign.show_header" v-model="localDesign.header_text"
            class="input text-sm" placeholder="e.g., @yourbrand" />
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-[#1c1c1e]">Footer</span>
            <Toggle v-model="localDesign.show_footer" />
          </div>
          <input v-if="localDesign.show_footer" v-model="localDesign.footer_text"
            class="input text-sm" placeholder="e.g., Swipe for more →" />
        </div>

        <!-- Per-slide layout overrides -->
        <div v-if="activeSlide" class="border-t border-[#f2f2f7] pt-1">
          <div class="flex items-center justify-between mb-3">
            <label class="label mb-0">This Slide Only</label>
            <button v-if="slideOv.padding != null || slideOv.show_header != null || slideOv.show_footer != null"
              class="text-[11px] text-[#ff3b30] font-semibold hover:underline"
              @click="setSlideOv({ padding: null, show_header: null, header_text: null, show_footer: null, footer_text: null })">
              Reset
            </button>
          </div>

          <!-- Padding override -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-1.5">
              <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold">Padding</label>
              <span class="text-xs text-[#0071e3] font-semibold">
                {{ slideOv.padding != null ? slideOv.padding + 'px' : 'Global' }}
              </span>
            </div>
            <input type="range" :value="slideOv.padding ?? localDesign.padding" min="0" max="120" step="4"
              @input="setSlideOv({ padding: parseInt(($event.target as HTMLInputElement).value) })" />
            <button v-if="slideOv.padding != null" class="text-[10px] text-[#ff3b30] font-semibold mt-1"
              @click="setSlideOv({ padding: null })">Use global</button>
          </div>

          <!-- Header override -->
          <div class="mb-3 space-y-2">
            <div class="flex items-center justify-between">
              <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold">Header</label>
              <div class="flex items-center gap-2">
                <button v-if="slideOv.show_header != null" class="text-[10px] text-[#ff3b30] font-semibold"
                  @click="setSlideOv({ show_header: null, header_text: null })">Use global</button>
                <Toggle :modelValue="slideOv.show_header ?? localDesign.show_header"
                  @update:modelValue="setSlideOv({ show_header: $event })" />
              </div>
            </div>
            <input v-if="slideOv.show_header ?? localDesign.show_header"
              :value="slideOv.header_text ?? ''"
              class="input text-sm" placeholder="Override header text…"
              @input="setSlideOv({ header_text: ($event.target as HTMLInputElement).value || null })" />
          </div>

          <!-- Footer override -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <label class="text-[11px] text-[#8e8e93] uppercase tracking-wide font-semibold">Footer</label>
              <div class="flex items-center gap-2">
                <button v-if="slideOv.show_footer != null" class="text-[10px] text-[#ff3b30] font-semibold"
                  @click="setSlideOv({ show_footer: null, footer_text: null })">Use global</button>
                <Toggle :modelValue="slideOv.show_footer ?? localDesign.show_footer"
                  @update:modelValue="setSlideOv({ show_footer: $event })" />
              </div>
            </div>
            <input v-if="slideOv.show_footer ?? localDesign.show_footer"
              :value="slideOv.footer_text ?? ''"
              class="input text-sm" placeholder="Override footer text…"
              @input="setSlideOv({ footer_text: ($event.target as HTMLInputElement).value || null })" />
          </div>
        </div>
      </template>
    </div>

    <!-- Actions -->
    <div class="shrink-0 px-4 pb-4 pt-3 border-t border-[#f2f2f7]">
      <button class="btn-secondary w-full text-sm" @click="$emit('apply-to-all', { ...localDesign })">
        Apply to All Slides
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CarouselDesign, FontChoice, Pattern, Slide, SlideOverrides } from "~/types"
import { FONT_FAMILIES } from "~/types"

const props = defineProps<{
  modelValue: CarouselDesign
  activeSlide?: Slide | null
}>()
const emit = defineEmits<{
  "update:modelValue": [CarouselDesign]
  "apply-to-all": [CarouselDesign]
  "update:slideOverrides": [SlideOverrides]
}>()

const config = useRuntimeConfig()
const activeTab = ref("template")
const uploading = ref(false)
const fileInput = ref<HTMLInputElement>()

const localDesign = reactive({ ...props.modelValue })

watch(() => props.modelValue, (v) => Object.assign(localDesign, v), { deep: true })
watch(localDesign, (v) => emit("update:modelValue", { ...v }), { deep: true })

// Per-slide style overrides — synced from activeSlide prop
const slideOv = reactive<SlideOverrides>({})

const syncSlideOv = (slide: Slide | null | undefined) => {
  slideOv.template        = slide?.overrides?.template        ?? null
  slideOv.accent_color    = slide?.overrides?.accent_color    ?? null
  slideOv.title_highlight = slide?.overrides?.title_highlight ?? null
  slideOv.align_h         = slide?.overrides?.align_h         ?? null
  slideOv.align_v         = slide?.overrides?.align_v         ?? null
  slideOv.pattern         = slide?.overrides?.pattern         ?? null
  slideOv.pattern_color   = slide?.overrides?.pattern_color   ?? null
  slideOv.pattern_opacity = slide?.overrides?.pattern_opacity ?? null
  slideOv.padding         = slide?.overrides?.padding         ?? null
  slideOv.show_header     = slide?.overrides?.show_header     ?? null
  slideOv.header_text     = slide?.overrides?.header_text     ?? null
  slideOv.show_footer     = slide?.overrides?.show_footer     ?? null
  slideOv.footer_text     = slide?.overrides?.footer_text     ?? null
}

watch(() => props.activeSlide, syncSlideOv, { immediate: true })

const setSlideOv = (patch: Partial<SlideOverrides>) => {
  Object.assign(slideOv, patch)
  emit("update:slideOverrides", { ...slideOv })
}

// --- Inline sub-components ---

// ColorSwatch: clickable color square that opens native picker
const ColorSwatch = defineComponent({
  props: { modelValue: String, value: String },
  emits: ["update:modelValue", "input"],
  setup(props, { emit }) {
    const color = computed(() => props.modelValue ?? props.value ?? "#000000")
    return () => h("div", { class: "relative shrink-0" }, [
      h("div", {
        class: "w-9 h-9 rounded-xl border border-[#d2d2d7] overflow-hidden cursor-pointer shadow-sm",
      }, [
        h("input", {
          type: "color",
          value: color.value,
          class: "absolute inset-0 w-full h-full cursor-pointer opacity-0",
          onInput: (e: Event) => {
            const v = (e.target as HTMLInputElement).value
            emit("update:modelValue", v)
            emit("input", e)
          },
        }),
        h("div", { class: "w-full h-full", style: { backgroundColor: color.value } }),
      ]),
    ])
  },
})

// Toggle: iOS-style switch
const Toggle = defineComponent({
  props: { modelValue: Boolean },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    return () => h("button", {
      class: `relative inline-flex h-6 w-10 items-center rounded-full transition-colors duration-150 ${props.modelValue ? "bg-[#0071e3]" : "bg-[#e5e5ea]"}`,
      onClick: () => emit("update:modelValue", !props.modelValue),
    }, [
      h("span", {
        class: `inline-block h-4 w-4 transform rounded-full bg-white shadow-sm transition-transform duration-150 ${props.modelValue ? "translate-x-5" : "translate-x-1"}`,
      }),
    ])
  },
})

const tabs = [
  {
    key: "template",
    label: "Style",
    icon: "M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z",
  },
  {
    key: "background",
    label: "BG",
    icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z",
  },
  {
    key: "typography",
    label: "Text",
    icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z",
  },
  {
    key: "layout",
    label: "Layout",
    icon: "M4 6h16M4 12h16M4 18h7",
  },
]

const patternOptions: { key: Pattern; label: string; svgPath: string; filled: boolean }[] = [
  {
    key: "none",
    label: "None",
    svgPath: "M5 5l10 10M15 5L5 15",
    filled: false,
  },
  {
    key: "dots1",
    label: "Dots S",
    svgPath: "M4 4a1 1 0 100-2 1 1 0 000 2zm6 0a1 1 0 100-2 1 1 0 000 2zm6 0a1 1 0 100-2 1 1 0 000 2zM4 10a1 1 0 100-2 1 1 0 000 2zm6 0a1 1 0 100-2 1 1 0 000 2zm6 0a1 1 0 100-2 1 1 0 000 2zM4 16a1 1 0 100-2 1 1 0 000 2zm6 0a1 1 0 100-2 1 1 0 000 2zm6 0a1 1 0 100-2 1 1 0 000 2z",
    filled: true,
  },
  {
    key: "dots2",
    label: "Dots M",
    svgPath: "M5 5a2 2 0 100-4 2 2 0 000 4zm10 0a2 2 0 100-4 2 2 0 000 4zM5 15a2 2 0 100-4 2 2 0 000 4zm10 0a2 2 0 100-4 2 2 0 000 4z",
    filled: true,
  },
  {
    key: "dots3",
    label: "Dots L",
    svgPath: "M7 7a3 3 0 100-6 3 3 0 000 6zm10 10a3 3 0 100-6 3 3 0 000 6z",
    filled: true,
  },
  {
    key: "grid",
    label: "Grid",
    svgPath: "M3 3h18v18H3V3zm6 0v18m6-18v18M3 9h18M3 15h18",
    filled: false,
  },
  {
    key: "lines",
    label: "Lines",
    svgPath: "M3 6h18M3 10h18M3 14h18M3 18h18",
    filled: false,
  },
  {
    key: "cells",
    label: "Cells",
    svgPath: "M3 3h7v7H3V3zm11 0h7v7h-7V3zM3 14h7v7H3v-7zm11 0h7v7h-7v-7z",
    filled: false,
  },
  {
    key: "blobs",
    label: "Blobs",
    svgPath: "M8 5c3 -1 6 1 7 4s-1 6 -4 7s-6 -1 -7 -4s1 -6 4 -7zm8 9c2 0 4 2 4 4s-2 4 -4 4s-4 -2 -4 -4s2 -4 4 -4z",
    filled: true,
  },
]

const sizeOptions: { key: "4:5" | "9:16" | "1:1"; label: string; sub: string }[] = [
  { key: "4:5",  label: "4:5 — 1080×1350",  sub: "Instagram Feed" },
  { key: "9:16", label: "9:16 — 1080×1920", sub: "Stories / Reels" },
  { key: "1:1",  label: "1:1 — 1080×1080",  sub: "Square Post" },
]

const fontOptions: { key: FontChoice; label: string; sample: string }[] = [
  { key: "system",       label: "System",      sample: "Aa" },
  { key: "playfair",     label: "Playfair",     sample: "Aa" },
  { key: "oswald",       label: "Oswald",       sample: "Aa" },
  { key: "montserrat",   label: "Montserrat",   sample: "Aa" },
  { key: "opensans",     label: "Open Sans",    sample: "Aa" },
  { key: "lato",         label: "Lato",         sample: "Aa" },
  { key: "merriweather", label: "Merriweather", sample: "Aa" },
  { key: "georgia",      label: "Georgia",      sample: "Aa" },
]

const templates = [
  { key: "bright",   label: "Bright",   bg: "#fff7ed", title: "#1c1917", body: "#44403c", accent: "#f97316", font: "'Roboto Condensed', Arial, sans-serif" },
  { key: "classic",  label: "Classic",  bg: "#ffffff",  title: "#1a1a1a", body: "#444444", accent: "#2563eb", font: "'Times New Roman', Times, serif" },
  { key: "comic",    label: "Comic",    bg: "#fef08a", title: "#18181b", body: "#3f3f46", accent: "#7c3aed", font: "'Fredoka', 'Arial Rounded MT Bold', sans-serif" },
  { key: "elegant",  label: "Elegant",  bg: "#0f172a", title: "#f8fafc", body: "#cbd5e1", accent: "#d4af37", font: "'Times New Roman', Times, serif" },
  { key: "minimal",  label: "Minimal",  bg: "#f8f8f6", title: "#222222", body: "#555555", accent: "#10b981", font: "'Jost', 'Helvetica Neue', sans-serif" },
  { key: "notes",    label: "Notes",    bg: "#fefce8", title: "#422006", body: "#78350f", accent: "#d97706", font: "'Caveat', cursive" },
  { key: "powerful", label: "Powerful", bg: "#09090b", title: "#fafafa", body: "#a1a1aa", accent: "#ef4444", font: "'Space Mono', 'Courier New', monospace" },
]

const setTemplate = (key: string) => {
  localDesign.template = key as any
  const t = templates.find((x) => x.key === key)
  if (t) {
    localDesign.bg_color = t.bg
    localDesign.title_font = "system"
    localDesign.body_font = "system"
  }
}

const handleImageUpload = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const form = new FormData()
    form.append("file", file)
    const resp = await $fetch<{ url: string }>(`${config.public.apiBase}/assets/upload`, {
      method: "POST", body: form,
    })
    localDesign.bg_image_url = resp.url
  } catch {
    alert("Upload failed")
  } finally {
    uploading.value = false
  }
}
</script>
