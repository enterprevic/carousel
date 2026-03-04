<template>
  <div class="flex flex-col h-full">
    <!-- Tabs -->
    <div class="flex shrink-0 px-2 pt-3 gap-1 overflow-x-auto">
      <button v-for="tab in tabs" :key="tab.key"
        class="px-3 py-1.5 text-xs font-medium rounded-lg whitespace-nowrap transition-all duration-150"
        :class="activeTab === tab.key
          ? 'bg-[#0071e3] text-white shadow-sm'
          : 'text-[#3a3a3c] hover:bg-black/5'"
        @click="activeTab = tab.key">
        {{ tab.label }}
      </button>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-5">

      <!-- Size -->
      <template v-if="activeTab === 'size'">
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
                <!-- Mini aspect ratio visual -->
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
      </template>

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
      </template>

      <!-- Background -->
      <template v-if="activeTab === 'background'">
        <div>
          <label class="label">Background Color</label>
          <div class="flex items-center gap-2.5">
            <div class="relative shrink-0">
              <div class="w-9 h-9 rounded-xl border border-[#d2d2d7] overflow-hidden cursor-pointer shadow-sm">
                <input type="color" v-model="localDesign.bg_color"
                  class="absolute inset-0 w-full h-full cursor-pointer opacity-0" />
                <div class="w-full h-full" :style="{ backgroundColor: localDesign.bg_color }" />
              </div>
            </div>
            <input v-model="localDesign.bg_color" class="input font-mono text-sm" placeholder="#ffffff" />
          </div>
        </div>

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
      </template>

      <!-- Pattern -->
      <template v-if="activeTab === 'pattern'">
        <div>
          <label class="label">Background Pattern</label>
          <div class="grid grid-cols-4 gap-1.5 mb-4">
            <button v-for="p in patternOptions" :key="p.key"
              class="flex flex-col items-center gap-1 py-2 rounded-xl border-2 transition-all duration-150"
              :class="(localDesign.pattern ?? 'none') === p.key
                ? 'border-[#0071e3] bg-[#0071e3]/5'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.pattern = p.key">
              <span class="text-base leading-none" :style="(localDesign.pattern ?? 'none') === p.key ? 'color:#0071e3' : 'color:#3a3a3c'">{{ p.icon }}</span>
              <span class="text-[9px] font-medium" :style="(localDesign.pattern ?? 'none') === p.key ? 'color:#0071e3' : 'color:#6c6c70'">{{ p.label }}</span>
            </button>
          </div>
        </div>

        <div v-if="localDesign.pattern && localDesign.pattern !== 'none'">
          <label class="label">Pattern Color</label>
          <div class="flex items-center gap-2.5 mb-4">
            <div class="relative shrink-0">
              <div class="w-9 h-9 rounded-xl border border-[#d2d2d7] overflow-hidden cursor-pointer shadow-sm">
                <input type="color" v-model="localDesign.pattern_color"
                  class="absolute inset-0 w-full h-full cursor-pointer opacity-0" />
                <div class="w-full h-full" :style="{ backgroundColor: localDesign.pattern_color }" />
              </div>
            </div>
            <input v-model="localDesign.pattern_color" class="input font-mono text-sm" placeholder="#000000" />
          </div>

          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="label mb-0">Pattern Opacity</label>
              <span class="text-xs text-[#0071e3] font-semibold">{{ Math.round((localDesign.pattern_opacity ?? 0.06) * 100) }}%</span>
            </div>
            <input type="range" v-model.number="localDesign.pattern_opacity" min="0.01" max="0.5" step="0.01" />
          </div>
        </div>

        <div>
          <label class="label">Accent Color</label>
          <p class="text-[11px] text-[#6c6c70] mb-2">Overrides the template's default accent (used for CTA text).</p>
          <div class="flex items-center gap-2.5">
            <div class="relative shrink-0">
              <div class="w-9 h-9 rounded-xl border border-[#d2d2d7] overflow-hidden cursor-pointer shadow-sm">
                <input type="color" :value="localDesign.accent_color || '#0071e3'"
                  class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                  @input="localDesign.accent_color = ($event.target as HTMLInputElement).value" />
                <div class="w-full h-full" :style="{ backgroundColor: localDesign.accent_color || '#e5e5ea' }" />
              </div>
            </div>
            <input :value="localDesign.accent_color || ''"
              class="input font-mono text-sm" placeholder="Template default"
              @input="localDesign.accent_color = ($event.target as HTMLInputElement).value || null" />
            <button v-if="localDesign.accent_color" class="text-xs text-[#ff3b30] font-medium whitespace-nowrap"
              @click="localDesign.accent_color = null">Reset</button>
          </div>
        </div>

        <div>
          <label class="label">Title Highlight</label>
          <p class="text-[11px] text-[#6c6c70] mb-2">Adds a background color behind the title text (marker effect).</p>
          <div class="flex items-center gap-2.5">
            <div class="relative shrink-0">
              <div class="w-9 h-9 rounded-xl border border-[#d2d2d7] overflow-hidden cursor-pointer shadow-sm">
                <input type="color" :value="localDesign.title_highlight || '#ffff00'"
                  class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                  @input="localDesign.title_highlight = ($event.target as HTMLInputElement).value" />
                <div class="w-full h-full" :style="{ backgroundColor: localDesign.title_highlight || '#e5e5ea' }" />
              </div>
            </div>
            <input :value="localDesign.title_highlight || ''"
              class="input font-mono text-sm" placeholder="No highlight"
              @input="localDesign.title_highlight = ($event.target as HTMLInputElement).value || null" />
            <button v-if="localDesign.title_highlight" class="text-xs text-[#ff3b30] font-medium whitespace-nowrap"
              @click="localDesign.title_highlight = null">Remove</button>
          </div>
        </div>
      </template>

      <!-- Layout -->
      <template v-if="activeTab === 'layout'">
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
                <path v-if="a === 'left'"    stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M3 12h12M3 18h8" />
                <path v-if="a === 'center'"  stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M6 12h12M7 18h10" />
                <path v-if="a === 'right'"   stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6h18M9 12h12M13 18h8" />
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
      </template>

      <!-- Fonts -->
      <template v-if="activeTab === 'fonts'">
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
      </template>

      <!-- Header / Footer -->
      <template v-if="activeTab === 'extras'">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-[#1c1c1e]">Header</span>
            <button class="relative inline-flex h-6 w-10 items-center rounded-full transition-colors duration-150"
              :class="localDesign.show_header ? 'bg-[#0071e3]' : 'bg-[#e5e5ea]'"
              @click="localDesign.show_header = !localDesign.show_header">
              <span class="inline-block h-4 w-4 transform rounded-full bg-white shadow-sm transition-transform duration-150"
                :class="localDesign.show_header ? 'translate-x-5' : 'translate-x-1'" />
            </button>
          </div>
          <input v-if="localDesign.show_header" v-model="localDesign.header_text"
            class="input text-sm" placeholder="e.g., @yourbrand" />
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-[#1c1c1e]">Footer</span>
            <button class="relative inline-flex h-6 w-10 items-center rounded-full transition-colors duration-150"
              :class="localDesign.show_footer ? 'bg-[#0071e3]' : 'bg-[#e5e5ea]'"
              @click="localDesign.show_footer = !localDesign.show_footer">
              <span class="inline-block h-4 w-4 transform rounded-full bg-white shadow-sm transition-transform duration-150"
                :class="localDesign.show_footer ? 'translate-x-5' : 'translate-x-1'" />
            </button>
          </div>
          <input v-if="localDesign.show_footer" v-model="localDesign.footer_text"
            class="input text-sm" placeholder="e.g., Swipe for more →" />
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
import type { CarouselDesign, FontChoice, Pattern } from "~/types"
import { FONT_FAMILIES } from "~/types"

const props = defineProps<{ modelValue: CarouselDesign }>()
const emit = defineEmits<{
  "update:modelValue": [CarouselDesign]
  "apply-to-all": [CarouselDesign]
}>()

const config = useRuntimeConfig()
const activeTab = ref("template")
const uploading = ref(false)
const fileInput = ref<HTMLInputElement>()

const localDesign = reactive({ ...props.modelValue })

watch(() => props.modelValue, (v) => Object.assign(localDesign, v), { deep: true })
watch(localDesign, (v) => emit("update:modelValue", { ...v }), { deep: true })

const tabs = [
  { key: "size",       label: "Size" },
  { key: "template",   label: "Template" },
  { key: "background", label: "Background" },
  { key: "pattern",    label: "Pattern" },
  { key: "layout",     label: "Layout" },
  { key: "fonts",      label: "Fonts" },
  { key: "extras",     label: "Header/Footer" },
]

const patternOptions: { key: Pattern; label: string; icon: string }[] = [
  { key: "none",  label: "None",   icon: "✕" },
  { key: "dots1", label: "Dots S", icon: "·" },
  { key: "dots2", label: "Dots M", icon: "•" },
  { key: "dots3", label: "Dots L", icon: "●" },
  { key: "grid",  label: "Grid",   icon: "⊞" },
  { key: "lines", label: "Lines",  icon: "≡" },
  { key: "cells", label: "Cells",  icon: "⊟" },
  { key: "blobs", label: "Blobs",  icon: "❍" },
]

const sizeOptions: { key: "4:5" | "9:16" | "1:1"; label: string; sub: string }[] = [
  { key: "4:5",  label: "4:5",  sub: "Instagram Feed" },
  { key: "9:16", label: "9:16", sub: "Stories / Reels" },
  { key: "1:1",  label: "1:1",  sub: "Square Post" },
]

const fontOptions: { key: FontChoice; label: string; sample: string }[] = [
  { key: "system",      label: "System",       sample: "Aa" },
  { key: "playfair",    label: "Playfair",      sample: "Aa" },
  { key: "oswald",      label: "Oswald",        sample: "Aa" },
  { key: "montserrat",  label: "Montserrat",    sample: "Aa" },
  { key: "opensans",    label: "Open Sans",     sample: "Aa" },
  { key: "lato",        label: "Lato",          sample: "Aa" },
  { key: "merriweather",label: "Merriweather",  sample: "Aa" },
  { key: "georgia",     label: "Georgia",       sample: "Aa" },
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
