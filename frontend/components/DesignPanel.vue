<template>
  <div class="flex flex-col h-full">
    <!-- Tabs -->
    <div class="flex shrink-0 px-2 pt-3 gap-1 overflow-x-auto">
      <button v-for="tab in tabs" :key="tab.key"
        class="px-3 py-1.5 text-xs font-medium rounded-lg whitespace-nowrap transition-all duration-150"
        :class="activeTab === tab.key
          ? 'bg-[#0071e3] text-white shadow-sm'
          : 'text-[#6e6e73] hover:bg-black/5'"
        @click="activeTab = tab.key">
        {{ tab.label }}
      </button>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-5">

      <!-- Template -->
      <template v-if="activeTab === 'template'">
        <div>
          <label class="label">Template</label>
          <div class="grid grid-cols-3 gap-2">
            <button v-for="t in templates" :key="t.key"
              class="rounded-xl overflow-hidden border-2 transition-all duration-150"
              :class="localDesign.template === t.key
                ? 'border-[#0071e3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7]'"
              @click="setTemplate(t.key)">
              <div class="h-14 flex flex-col items-center justify-center gap-0.5 px-2" :style="{ background: t.bg }">
                <div class="font-bold truncate w-full text-center" :style="{ color: t.title, fontSize: '6px' }">TITLE</div>
                <div class="truncate w-full text-center" :style="{ color: t.body, fontSize: '5px' }">Body text here</div>
              </div>
              <div class="py-1.5 text-center text-[10px] font-medium text-[#6e6e73] bg-white">
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
                : 'bg-white text-[#6e6e73] border-[#e5e5ea] hover:border-[#d2d2d7]'"
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
                : 'bg-white text-[#6e6e73] border-[#e5e5ea] hover:border-[#d2d2d7]'"
              @click="localDesign.align_v = a as any">
              {{ a }}
            </button>
          </div>
        </div>
      </template>

      <!-- Header / Footer -->
      <template v-if="activeTab === 'extras'">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-[#1d1d1f]">Header</span>
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
            <span class="text-sm font-medium text-[#1d1d1f]">Footer</span>
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
    <div class="shrink-0 px-4 pb-4 pt-3 border-t border-[#f5f5f7] space-y-2">
      <button class="btn-secondary w-full text-sm" @click="$emit('apply-to-all', { ...localDesign })">
        Apply to All Slides
      </button>
      <button class="btn-primary w-full text-sm" :disabled="saving" @click="$emit('save', { ...localDesign })">
        {{ saving ? 'Saving…' : 'Save Design' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CarouselDesign } from "~/types"

const props = defineProps<{ modelValue: CarouselDesign; saving?: boolean }>()
const emit = defineEmits<{
  "update:modelValue": [CarouselDesign]
  save: [CarouselDesign]
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
  { key: "template",   label: "Template" },
  { key: "background", label: "Background" },
  { key: "layout",     label: "Layout" },
  { key: "extras",     label: "Header/Footer" },
]

const templates = [
  { key: "classic", label: "Classic", bg: "#ffffff", title: "#1a1a1a", body: "#444444" },
  { key: "bold",    label: "Bold",    bg: "#0f0f0f", title: "#ffffff", body: "#e0e0e0" },
  { key: "minimal", label: "Minimal", bg: "#f8f8f6", title: "#222222", body: "#555555" },
]

const setTemplate = (key: string) => {
  localDesign.template = key as any
  const t = templates.find((x) => x.key === key)
  if (t) localDesign.bg_color = t.bg
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
