<template>
  <div class="flex flex-col h-full">
    <!-- Tabs -->
    <div v-if="!hideTabBar" class="shrink-0 px-3 pt-3 pb-0">
      <div class="flex gap-0.5 bg-[#F4F5F6] rounded-xl p-1">
        <button v-for="tab in tabs" :key="tab.key"
          class="flex-1 flex flex-col items-center gap-0.5 py-1.5 px-1 rounded-lg text-[10px] font-medium transition-all duration-150 leading-tight"
          :class="activeTab === tab.key
            ? 'bg-white text-[#2B31B3] shadow-sm'
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
                ? 'border-[#2B31B3] shadow-[0_0_0_3px_rgba(0,113,227,0.15)]'
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
        <!-- Тип фона -->
        <div>
          <label class="label">Тип фона</label>
          <div class="flex gap-2 mb-3">
            <button
              class="flex-1 py-2 rounded-xl border-2 text-sm font-medium transition-all duration-150"
              :class="!localDesign.bg_image_url ? 'border-[#2B31B3] bg-[#EEF0FF] text-[#2B31B3]' : 'border-[#e5e5ea] text-[#4E616B] hover:border-[#d2d2d7]'"
              @click="localDesign.bg_image_url = null">
              Цвет
            </button>
            <button
              class="flex-1 py-2 rounded-xl border-2 text-sm font-medium transition-all duration-150"
              :class="localDesign.bg_image_url ? 'border-[#2B31B3] bg-[#EEF0FF] text-[#2B31B3]' : 'border-[#e5e5ea] text-[#4E616B] hover:border-[#d2d2d7]'"
              @click="(fileInput as HTMLInputElement)?.click()">
              Фото
            </button>
          </div>
          <input type="file" accept="image/*" ref="fileInput" class="hidden" @change="handleImageUpload" />

          <!-- Color mode -->
          <div v-if="!localDesign.bg_image_url" class="flex items-center gap-2.5">
            <ColorSwatch v-model="localDesign.bg_color" />
            <input v-model="localDesign.bg_color" class="input font-mono text-sm" placeholder="#ffffff" />
          </div>

          <!-- Photo mode -->
          <div v-else class="space-y-3">
            <button class="btn-secondary w-full text-sm" :disabled="uploading" @click="(fileInput as HTMLInputElement)?.click()">
              <svg v-if="uploading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ uploading ? 'Загрузка…' : 'Выбрать фото' }}
            </button>
            <div class="flex items-center gap-2.5">
              <img :src="localDesign.bg_image_url" class="w-12 h-12 object-cover rounded-xl border border-[#e5e5ea]" />
              <button class="text-xs text-[#ff3b30] font-medium hover:underline" @click="localDesign.bg_image_url = null">Удалить</button>
            </div>
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="label mb-0">Затемнение</label>
                <span class="text-xs text-[#2B31B3] font-semibold">{{ Math.round(localDesign.darkening * 100) }}%</span>
              </div>
              <input type="range" v-model.number="localDesign.darkening" min="0" max="0.9" step="0.05" />
            </div>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <!-- Акцентный цвет -->
        <div>
          <label class="label">Акцентный цвет</label>
          <div class="flex items-center gap-2.5">
            <ColorSwatch
              :value="localDesign.accent_color || '#2B31B3'"
              @input="localDesign.accent_color = ($event.target as HTMLInputElement).value" />
            <input :value="localDesign.accent_color || ''"
              class="input font-mono text-sm" placeholder="По умолчанию шаблона"
              @input="localDesign.accent_color = ($event.target as HTMLInputElement).value || null" />
            <button v-if="localDesign.accent_color" class="text-xs text-[#ff3b30] font-medium whitespace-nowrap"
              @click="localDesign.accent_color = null">✕</button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <!-- Узор -->
        <div>
          <label class="label">Узор</label>
          <div class="grid grid-cols-4 gap-1.5">
            <button v-for="p in patternOptions" :key="p.key"
              class="flex flex-col items-center gap-1 py-2 rounded-xl border-2 transition-all duration-150"
              :class="(localDesign.pattern ?? 'none') === p.key
                ? 'border-[#2B31B3] bg-[#2B31B3]/5'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.pattern = p.key">
              <svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"
                :style="(localDesign.pattern ?? 'none') === p.key ? 'color:#2B31B3' : 'color:#8e8e93'">
                <path :d="p.svgPath" :fill="p.filled ? 'currentColor' : 'none'"
                  :stroke="p.filled ? 'none' : 'currentColor'" stroke-width="1.2" />
              </svg>
              <span class="text-[9px] font-medium"
                :style="(localDesign.pattern ?? 'none') === p.key ? 'color:#2B31B3' : 'color:#6c6c70'">{{ p.label }}</span>
            </button>
          </div>
          <div v-if="localDesign.pattern && localDesign.pattern !== 'none'" class="mt-3 space-y-3">
            <div class="flex items-center gap-2.5">
              <ColorSwatch v-model="localDesign.pattern_color" />
              <input v-model="localDesign.pattern_color" class="input font-mono text-sm" placeholder="#000000" />
            </div>
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="label mb-0">Прозрачность</label>
                <span class="text-xs text-[#2B31B3] font-semibold">{{ Math.round((localDesign.pattern_opacity ?? 0.06) * 100) }}%</span>
              </div>
              <input type="range" v-model.number="localDesign.pattern_opacity" min="0.01" max="0.5" step="0.01" />
            </div>
          </div>
        </div>
      </template>

      <!-- Typography -->
      <template v-if="activeTab === 'typography'">
        <!-- Цвет выделения -->
        <div>
          <label class="label">Цвет выделения</label>
          <p class="text-[11px] text-[#6c6c70] mb-2 -mt-1">Маркерный фон за текстом заголовка.</p>
          <div class="flex items-center gap-2.5">
            <ColorSwatch
              :value="localDesign.title_highlight || '#ffff00'"
              @input="localDesign.title_highlight = ($event.target as HTMLInputElement).value" />
            <input :value="localDesign.title_highlight || ''"
              class="input font-mono text-sm" placeholder="Без выделения"
              @input="localDesign.title_highlight = ($event.target as HTMLInputElement).value || null" />
            <button v-if="localDesign.title_highlight"
              class="text-xs text-[#ff3b30] font-medium whitespace-nowrap"
              @click="localDesign.title_highlight = null">✕</button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <!-- Шрифт заголовка -->
        <div>
          <label class="label">Шрифт заголовка</label>
          <div class="grid grid-cols-2 gap-1.5">
            <button v-for="f in titleFontOptions" :key="f.key"
              class="rounded-xl border-2 py-2 px-2 text-left transition-all duration-150"
              :class="(localDesign.title_font ?? 'system') === f.key
                ? 'border-[#2B31B3] bg-[#2B31B3]/5 shadow-sm'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.title_font = f.key">
              <div class="text-base font-bold leading-none mb-0.5 text-[#000000]"
                :style="{ fontFamily: FONT_FAMILIES[f.key] }">
                Aa
              </div>
              <div class="text-[10px] text-[#6c6c70] truncate">{{ f.label }}</div>
            </button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <!-- Шрифт текста -->
        <div>
          <label class="label">Шрифт текста</label>
          <div class="grid grid-cols-2 gap-1.5">
            <button v-for="f in bodyFontOptions" :key="f.key"
              class="rounded-xl border-2 py-2 px-2 text-left transition-all duration-150"
              :class="(localDesign.body_font ?? 'system') === f.key
                ? 'border-[#2B31B3] bg-[#2B31B3]/5 shadow-sm'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.body_font = f.key">
              <div class="text-base leading-none mb-0.5 text-[#000000]"
                :style="{ fontFamily: FONT_FAMILIES[f.key] }">
                Aa
              </div>
              <div class="text-[10px] text-[#6c6c70] truncate">{{ f.label }}</div>
            </button>
          </div>
        </div>
      </template>

      <!-- Layout -->
      <template v-if="activeTab === 'layout'">
        <!-- Image size -->
        <div>
          <label class="label">Размер изображения</label>
          <div class="flex flex-col gap-2">
            <button v-for="s in sizeOptions" :key="s.key"
              class="flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all duration-150 text-left"
              :class="(localDesign.aspect_ratio ?? '4:5') === s.key
                ? 'border-[#2B31B3] bg-[#2B31B3]/5 shadow-sm'
                : 'border-[#e5e5ea] hover:border-[#d2d2d7] bg-white'"
              @click="localDesign.aspect_ratio = s.key">
              <div class="shrink-0 flex items-center justify-center w-8"
                :class="(localDesign.aspect_ratio ?? '4:5') === s.key ? 'text-[#2B31B3]' : 'text-[#8e8e93]'">
                <div class="border-2 rounded"
                  :class="(localDesign.aspect_ratio ?? '4:5') === s.key ? 'border-[#2B31B3]' : 'border-[#c6c6c8]'"
                  :style="s.key === '4:5'  ? 'width:16px;height:20px' :
                          s.key === '9:16' ? 'width:12px;height:20px' :
                                             'width:20px;height:20px'" />
              </div>
              <div>
                <div class="text-sm font-semibold text-[#000000]">{{ s.label }}</div>
                <div class="text-xs text-[#6c6c70]">{{ s.sub }}</div>
              </div>
            </button>
          </div>
        </div>

        <div class="border-t border-[#f2f2f7]" />

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="label mb-0">Отступ содержимого</label>
            <span class="text-xs text-[#2B31B3] font-semibold">{{ localDesign.padding }}px</span>
          </div>
          <input type="range" v-model.number="localDesign.padding" min="20" max="80" step="4" />
        </div>

        <!-- Выравнивание: horizontal + vertical on one row -->
        <div>
          <label class="label">Выравнивание</label>
          <div class="flex flex-col gap-2">
            <!-- По горизонтали -->
            <div class="flex items-center gap-2">
              <span class="text-xs text-[#6c6c70] w-24 shrink-0">По горизонтали</span>
              <div class="flex gap-1">
                <button v-for="a in hAlignOptions" :key="a.key"
                  class="w-8 h-8 flex items-center justify-center rounded-lg border transition-all duration-150"
                  :class="localDesign.align_h === a.key
                    ? 'bg-[#2B31B3] text-white border-[#2B31B3]'
                    : 'bg-white text-[#3a3a3c] border-[#c6c6c8] hover:border-[#8e8e93]'"
                  :title="a.title"
                  @click="localDesign.align_h = a.key as any">
                  <svg class="w-[15px] h-[15px]" viewBox="0 0 24 24" fill="currentColor">
                    <path v-for="(p, i) in a.paths" :key="i" :d="p" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- По вертикали -->
            <div class="flex items-center gap-2">
              <span class="text-xs text-[#6c6c70] w-24 shrink-0">По вертикали</span>
              <div class="flex gap-1">
                <button v-for="a in verticalAlignOptions" :key="a.key"
                  class="w-8 h-8 flex items-center justify-center rounded-lg border transition-all duration-150"
                  :class="localDesign.align_v === a.key
                    ? 'bg-[#2B31B3] text-white border-[#2B31B3]'
                    : 'bg-white text-[#3a3a3c] border-[#c6c6c8] hover:border-[#8e8e93]'"
                  :title="a.title"
                  @click="localDesign.align_v = a.key as any">
                  <svg v-if="a.key === 'spread'" class="w-[15px] h-[15px]" viewBox="0 0 256 256" fill="currentColor">
                    <path v-for="(p, i) in a.paths" :key="i" :d="p" />
                  </svg>
                  <svg v-else class="w-[15px] h-[15px]" viewBox="0 0 24 24" fill="currentColor">
                    <path v-for="(p, i) in a.paths" :key="i" :d="p" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

      </template>

      <!-- Extra -->
      <template v-if="activeTab === 'extra'">
        <div class="space-y-4">
          <!-- Показывать шапку -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-[#000000]">Показывать шапку</span>
              <Toggle v-model="localDesign.show_header" />
            </div>
            <input v-if="localDesign.show_header" v-model="localDesign.header_text"
              class="input text-sm" placeholder="Напр., @yourbrand" />
          </div>

          <div class="border-t border-[#f2f2f7]" />

          <!-- Показывать подвал -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-[#000000]">Показывать подвал</span>
              <Toggle v-model="localDesign.show_footer" />
            </div>
            <input v-if="localDesign.show_footer" v-model="localDesign.footer_text"
              class="input text-sm" placeholder="Напр., Листайте дальше →" />
          </div>
        </div>
      </template>
    </div>

    <!-- Actions -->
    <div class="shrink-0 px-4 pb-4 pt-3 border-t border-[#f2f2f7] space-y-2">
      <button class="w-full py-2 rounded-xl border border-[#E6E8EA] text-sm text-[#4E616B] hover:bg-[#F4F5F6] transition-colors font-medium"
        @click="$emit('apply-to-all', { ...localDesign })">
        Применить ко всем слайдам
      </button>
      <div class="flex gap-2">
        <button class="flex-1 py-2 rounded-xl border border-[#E6E8EA] text-sm text-[#4E616B] hover:bg-[#F4F5F6] transition-colors font-medium"
          @click="$emit('cancel')">
          Отмена
        </button>
        <button class="flex-1 py-2 rounded-xl bg-[#2B31B3] text-white text-sm font-semibold hover:bg-[#2228a0] transition-colors"
          @click="handleApply">
          Применить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CarouselDesign, FontChoice, Pattern, Slide, SlideOverrides } from "~/types"
import { FONT_FAMILIES } from "~/types"
const { t } = useLang()

const props = defineProps<{
  modelValue: CarouselDesign
  activeSlide?: Slide | null
  initialTab?: string
  hideTabBar?: boolean
}>()
const emit = defineEmits<{
  "update:modelValue": [CarouselDesign]
  "apply-to-all": [CarouselDesign]
  "update:slideOverrides": [SlideOverrides]
  "cancel": []
}>()

const config = useRuntimeConfig()
const { authHeaders } = useAuth()
const activeTab = ref(props.initialTab ?? "template")

watch(() => props.initialTab, (v) => { if (v) activeTab.value = v })
const uploading = ref(false)
const fileInput = ref<HTMLInputElement>()

const localDesign = reactive({ ...props.modelValue })

watch(() => props.modelValue, (v) => Object.assign(localDesign, v), { deep: true, immediate: true })
// Live preview: propagate localDesign changes up immediately so SlidePreview re-renders instantly
watch(localDesign, (v) => emit("update:modelValue", { ...v }), { deep: true, flush: 'sync' })

// "Применить" = save as per-slide overrides (current slide only)
const handleApply = () => {
  const ov: SlideOverrides = {
    bg_color:        localDesign.bg_color,
    bg_image_url:    localDesign.bg_image_url,
    darkening:       localDesign.darkening,
    template:        localDesign.template as any,
    accent_color:    localDesign.accent_color,
    title_highlight: localDesign.title_highlight,
    align_h:         localDesign.align_h,
    align_v:         localDesign.align_v,
    pattern:         localDesign.pattern as any,
    pattern_color:   localDesign.pattern_color,
    pattern_opacity: localDesign.pattern_opacity,
    padding:         localDesign.padding,
    show_header:     localDesign.show_header,
    header_text:     localDesign.header_text,
    show_footer:     localDesign.show_footer,
    footer_text:     localDesign.footer_text,
  }
  emit("update:slideOverrides", ov)
}

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

// Toggle: iOS-style switch with visible border outline
const Toggle = defineComponent({
  props: { modelValue: Boolean },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    return () => h("button", {
      class: `relative inline-flex h-6 w-11 shrink-0 items-center rounded-full border-2 transition-colors duration-200 focus:outline-none ${props.modelValue ? "bg-[#2B31B3] border-[#2B31B3]" : "bg-white border-[#c6c6c8]"}`,
      onClick: () => emit("update:modelValue", !props.modelValue),
    }, [
      h("span", {
        class: `inline-block h-4 w-4 transform rounded-full shadow transition-transform duration-200 ${props.modelValue ? "translate-x-5 bg-white" : "translate-x-0.5 bg-[#c6c6c8]"}`,
      }),
    ])
  },
})

const tabs = computed(() => [
  {
    key: "template",
    label: t.value.tabTemplate,
    icon: "M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z",
  },
  {
    key: "background",
    label: t.value.tabBackground,
    icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z",
  },
  {
    key: "typography",
    label: t.value.tabTypography,
    icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z",
  },
  {
    key: "layout",
    label: t.value.tabLayout,
    icon: "M4 6h16M4 12h16M4 18h7",
  },
])

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

// Exact CiAlign* paths from react-icons/ci (Circum Icons)
const hAlignOptions = [
  {
    key: "left", title: "По левому краю",
    // CiAlignLeft: vertical bar at left + two rectangles of different widths
    paths: [
      "M3.078,3.548v16.9a.5.5,0,0,0,1,0V3.548a.5.5,0,0,0-1,0Z",
      "M18.422,11.5H7.582A2.5,2.5,0,0,1,5.082,9V6.565a2.5,2.5,0,0,1,2.5-2.5h10.84a2.5,2.5,0,0,1,2.5,2.5V9A2.5,2.5,0,0,1,18.422,11.5ZM7.582,5.065a1.5,1.5,0,0,0-1.5,1.5V9a1.5,1.5,0,0,0,1.5,1.5h10.84a1.5,1.5,0,0,0,1.5-1.5V6.565a1.5,1.5,0,0,0-1.5-1.5Z",
      "M13.451,19.938H7.582a2.5,2.5,0,0,1-2.5-2.5V15a2.5,2.5,0,0,1,2.5-2.5h5.869a2.5,2.5,0,0,1,2.5,2.5v2.436A2.5,2.5,0,0,1,13.451,19.938ZM7.582,13.5a1.5,1.5,0,0,0-1.5,1.5v2.436a1.5,1.5,0,0,0,1.5,1.5h5.869a1.5,1.5,0,0,0,1.5-1.5V15a1.5,1.5,0,0,0-1.5-1.5Z",
    ],
  },
  {
    key: "center", title: "По центру",
    // CiAlignCenterV: center vertical bar + two rectangles centered
    paths: [
      "M20.446,11.5h-.51V9.07a2.5,2.5,0,0,0-2.5-2.5h-2.43a2.5,2.5,0,0,0-2.5,2.5V11.5H11.5V6.58A2.5,2.5,0,0,0,9,4.08H6.566a2.5,2.5,0,0,0-2.5,2.5V11.5h-.52a.5.5,0,0,0,0,1h.52v4.92a2.5,2.5,0,0,0,2.5,2.5H9a2.5,2.5,0,0,0,2.5-2.5V12.5h1.01v2.43a2.5,2.5,0,0,0,2.5,2.5h2.43a2.5,2.5,0,0,0,2.5-2.5V12.5h.51A.5.5,0,0,0,20.446,11.5ZM10.5,17.42A1.5,1.5,0,0,1,9,18.92H6.566a1.5,1.5,0,0,1-1.5-1.5V12.5H10.5Zm0-5.92H5.066V6.58a1.5,1.5,0,0,1,1.5-1.5H9a1.5,1.5,0,0,1,1.5,1.5Zm8.44,3.43a1.5,1.5,0,0,1-1.5,1.5h-2.43a1.5,1.5,0,0,1-1.5-1.5V12.5h5.43Zm0-3.43h-5.43V9.07a1.5,1.5,0,0,1,1.5-1.5h2.43a1.5,1.5,0,0,1,1.5,1.5Z",
    ],
  },
  {
    key: "right", title: "По правому краю",
    // CiAlignRight: vertical bar at right + two rectangles flush right
    paths: [
      "M19.922,3.548v16.9a.5.5,0,0,0,1,0V3.548a.5.5,0,0,0-1,0Z",
      "M16.419,11.5H5.578A2.5,2.5,0,0,1,3.078,9V6.565a2.5,2.5,0,0,1,2.5-2.5H16.419a2.5,2.5,0,0,1,2.5,2.5V9A2.5,2.5,0,0,1,16.419,11.5ZM5.578,5.065a1.5,1.5,0,0,0-1.5,1.5V9a1.5,1.5,0,0,0,1.5,1.5H16.419a1.5,1.5,0,0,0,1.5-1.5V6.565a1.5,1.5,0,0,0-1.5-1.5Z",
      "M16.419,19.938H10.55a2.5,2.5,0,0,1-2.5-2.5V15a2.5,2.5,0,0,1,2.5-2.5h5.869a2.5,2.5,0,0,1,2.5,2.5v2.436A2.5,2.5,0,0,1,16.419,19.938ZM10.55,13.5A1.5,1.5,0,0,0,9.05,15v2.436a1.5,1.5,0,0,0,1.5,1.5h5.869a1.5,1.5,0,0,0,1.5-1.5V15a1.5,1.5,0,0,0-1.5-1.5Z",
    ],
  },
]

// Exact CiAlign* vertical paths
const verticalAlignOptions = [
  {
    key: "top", title: "Сверху",
    // CiAlignTop: horizontal bar at top + two rectangles flush top
    paths: [
      "M3.548,4.078h16.9a.5.5,0,0,0,0-1H3.548a.5.5,0,0,0,0,1Z",
      "M9,20.922H6.565a2.5,2.5,0,0,1-2.5-2.5V7.582a2.5,2.5,0,0,1,2.5-2.5H9a2.5,2.5,0,0,1,2.5,2.5v10.84A2.5,2.5,0,0,1,9,20.922ZM6.565,6.082a1.5,1.5,0,0,0-1.5,1.5v10.84a1.5,1.5,0,0,0,1.5,1.5H9a1.5,1.5,0,0,0,1.5-1.5V7.582A1.5,1.5,0,0,0,9,6.082Z",
      "M17.438,15.951H15a2.5,2.5,0,0,1-2.5-2.5V7.582a2.5,2.5,0,0,1,2.5-2.5h2.435a2.5,2.5,0,0,1,2.5,2.5v5.869A2.5,2.5,0,0,1,17.438,15.951ZM15,6.082a1.5,1.5,0,0,0-1.5,1.5v5.869a1.5,1.5,0,0,0,1.5,1.5h2.435a1.5,1.5,0,0,0,1.5-1.5V7.582a1.5,1.5,0,0,0-1.5-1.5Z",
    ],
  },
  {
    key: "center", title: "По центру",
    // CiAlignCenterH: center horizontal bar + two rectangles centered
    paths: [
      "M17.42,4.062H12.5v-.51a.5.5,0,0,0-1,0v.51H6.58a2.507,2.507,0,0,0-2.5,2.5V9a2.5,2.5,0,0,0,2.5,2.5H11.5v1H9.06A2.507,2.507,0,0,0,6.56,15v2.44a2.507,2.507,0,0,0,2.5,2.5H11.5v.51a.5.5,0,0,0,1,0v-.51h2.43a2.5,2.5,0,0,0,2.5-2.5V15a2.5,2.5,0,0,0-2.5-2.5H12.5v-1h4.92A2.5,2.5,0,0,0,19.92,9V6.562A2.507,2.507,0,0,0,17.42,4.062ZM11.5,18.942H9.06a1.511,1.511,0,0,1-1.5-1.5V15a1.5,1.5,0,0,1,1.5-1.5H11.5Zm0-8.44H6.58A1.5,1.5,0,0,1,5.08,9V6.562a1.5,1.5,0,0,1,1.5-1.5H11.5Zm3.43,3a1.5,1.5,0,0,1,1.5,1.5v2.44a1.5,1.5,0,0,1-1.5,1.5H12.5V13.5ZM18.92,9a1.5,1.5,0,0,1-1.5,1.5H12.5V5.062h4.92a1.5,1.5,0,0,1,1.5,1.5Z",
    ],
  },
  {
    key: "bottom", title: "Снизу",
    // CiAlignBottom: horizontal bar at bottom + two rectangles flush bottom
    paths: [
      "M3.548,20.922h16.9a.5.5,0,0,0,0-1H3.548a.5.5,0,0,0,0,1Z",
      "M9,18.919H6.565a2.5,2.5,0,0,1-2.5-2.5V5.578a2.5,2.5,0,0,1,2.5-2.5H9a2.5,2.5,0,0,1,2.5,2.5V16.419A2.5,2.5,0,0,1,9,18.919ZM6.565,4.078a1.5,1.5,0,0,0-1.5,1.5V16.419a1.5,1.5,0,0,0,1.5,1.5H9a1.5,1.5,0,0,0,1.5-1.5V5.578A1.5,1.5,0,0,0,9,4.078Z",
      "M17.437,18.919H15a2.5,2.5,0,0,1-2.5-2.5V10.55A2.5,2.5,0,0,1,15,8.05h2.434a2.5,2.5,0,0,1,2.5,2.5v5.869A2.5,2.5,0,0,1,17.437,18.919ZM15,9.05a1.5,1.5,0,0,0-1.5,1.5v5.869a1.5,1.5,0,0,0,1.5,1.5h2.434a1.5,1.5,0,0,0,1.5-1.5V10.55a1.5,1.5,0,0,0-1.5-1.5Z",
    ],
  },
  {
    key: "spread", title: "Растянуть",
    // PiArrowsOutLineVertical (viewBox 0 0 256 256)
    paths: [
      "M224,128a8,8,0,0,1-8,8H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,128ZM101.66,53.66,120,35.31V96a8,8,0,0,0,16,0V35.31l18.34,18.35a8,8,0,0,0,11.32-11.32l-32-32a8,8,0,0,0-11.32,0l-32,32a8,8,0,0,0,11.32,11.32Zm52.68,148.68L136,220.69V160a8,8,0,0,0-16,0v60.69l-18.34-18.35a8,8,0,0,0-11.32,11.32l32,32a8,8,0,0,0,11.32,0l32-32a8,8,0,0,0-11.32-11.32Z",
    ],
  },
]

const titleFontOptions: { key: FontChoice; label: string }[] = [
  { key: "system",          label: "System" },
  { key: "inter",           label: "Inter" },
  { key: "firacode",        label: "Fira Code" },
  { key: "roboto_condensed",label: "Roboto Condensed" },
  { key: "jost",            label: "Jost" },
  { key: "caveat",          label: "Caveat" },
  { key: "source_sans3",    label: "Source Sans 3" },
]

const bodyFontOptions: { key: FontChoice; label: string }[] = [
  { key: "system",  label: "System" },
  { key: "inter",   label: "Inter" },
  { key: "firacode",label: "Fira Code" },
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
      method: "POST", headers: authHeaders(), body: form,
    })
    localDesign.bg_image_url = resp.url
  } catch {
    alert("Upload failed")
  } finally {
    uploading.value = false
  }
}
</script>
