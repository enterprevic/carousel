<template>
  <div class="min-h-screen bg-[#f5f5f7]">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-[#fbfbfd]/90 backdrop-blur-xl border-b border-black/[0.06]">
      <div class="max-w-2xl mx-auto px-5 h-14 flex items-center gap-3">
        <NuxtLink to="/" class="w-8 h-8 rounded-xl flex items-center justify-center
          text-[#6e6e73] hover:bg-black/5 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </NuxtLink>
        <h1 class="font-semibold text-[#1d1d1f] tracking-tight">New Carousel</h1>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-5 py-8">
      <!-- Step indicator -->
      <div class="flex items-center gap-1.5 mb-10">
        <div v-for="(s, i) in steps" :key="i" class="flex items-center gap-1.5 flex-1">
          <div class="flex items-center gap-2 shrink-0">
            <div class="w-6 h-6 rounded-full flex items-center justify-center text-[11px] font-bold transition-all duration-200"
              :class="step > i
                ? 'bg-[#0071e3] text-white'
                : step === i
                  ? 'bg-[#0071e3] text-white ring-4 ring-[#0071e3]/20'
                  : 'bg-[#e5e5ea] text-[#aeaeb2]'">
              <svg v-if="step > i" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
              <span v-else>{{ i + 1 }}</span>
            </div>
            <span class="text-xs font-medium hidden sm:block"
              :class="step >= i ? 'text-[#1d1d1f]' : 'text-[#aeaeb2]'">{{ s }}</span>
          </div>
          <div v-if="i < steps.length - 1"
            class="flex-1 h-px mx-1 hidden sm:block transition-colors duration-300"
            :class="step > i ? 'bg-[#0071e3]' : 'bg-[#e5e5ea]'" />
        </div>
      </div>

      <!-- Step 1: Source Type -->
      <div v-if="step === 0">
        <h2 class="text-2xl font-bold text-[#1d1d1f] tracking-tight mb-1">Choose your source</h2>
        <p class="text-[#6e6e73] text-sm mb-7">How do you want to create your carousel?</p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button v-for="type in sourceTypes" :key="type.key"
            class="relative text-left p-5 rounded-2xl border-2 transition-all duration-150 bg-white"
            :class="sourceType === type.key
              ? 'border-[#0071e3] shadow-[0_0_0_4px_rgba(0,113,227,0.1)]'
              : 'border-transparent shadow-[0_2px_12px_rgba(0,0,0,0.07)] hover:shadow-[0_4px_16px_rgba(0,0,0,0.1)] hover:-translate-y-0.5'"
            @click="sourceType = type.key">
            <div class="text-2xl mb-3">{{ type.icon }}</div>
            <h3 class="font-semibold text-[#1d1d1f] text-sm mb-1">{{ type.label }}</h3>
            <p class="text-[#6e6e73] text-xs leading-relaxed">{{ type.desc }}</p>
            <div v-if="sourceType === type.key"
              class="absolute top-3 right-3 w-5 h-5 bg-[#0071e3] rounded-full flex items-center justify-center">
              <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </button>
        </div>
        <div class="flex justify-end mt-8">
          <button class="btn-primary px-6" :disabled="!sourceType" @click="step = 1">Continue</button>
        </div>
      </div>

      <!-- Step 2: Content Input -->
      <div v-else-if="step === 1">
        <h2 class="text-2xl font-bold text-[#1d1d1f] tracking-tight mb-1">Add your content</h2>
        <p class="text-[#6e6e73] text-sm mb-7">Provide the source material for your carousel</p>

        <div class="card p-6 space-y-5">
          <div>
            <label class="label">Title</label>
            <input v-model="title" class="input" placeholder="e.g., 5 tips for better sleep" />
          </div>

          <!-- Text -->
          <template v-if="sourceType === 'text'">
            <div>
              <label class="label">Source Text</label>
              <textarea v-model="sourceText" class="input min-h-[180px] resize-y leading-relaxed"
                placeholder="Paste your article, notes, or any text to turn into a carousel…" />
            </div>
          </template>

          <!-- Video -->
          <template v-else-if="sourceType === 'video'">
            <div>
              <label class="label">Video URL</label>
              <input v-model="videoUrl" class="input" placeholder="https://youtube.com/watch?v=…" />
            </div>
            <div>
              <label class="label">Notes <span class="text-[#aeaeb2] normal-case font-normal tracking-normal">— optional</span></label>
              <textarea v-model="videoNotes" class="input min-h-[100px] resize-y"
                placeholder="Key points, timestamps, or context to include…" />
            </div>
          </template>

          <!-- Links -->
          <template v-else-if="sourceType === 'links'">
            <div>
              <label class="label">Links</label>
              <div class="space-y-2">
                <div v-for="(link, i) in links" :key="i" class="flex gap-2">
                  <input v-model="links[i]" class="input flex-1" :placeholder="`https://… (link ${i + 1})`" />
                  <button class="btn-ghost w-9 h-9 p-0 rounded-xl text-[#ff3b30]" @click="links.splice(i, 1)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <button class="btn-ghost text-xs text-[#0071e3] px-0" @click="links.push('')">
                  + Add link
                </button>
              </div>
            </div>
            <div>
              <label class="label">Notes</label>
              <textarea v-model="sourceText" class="input min-h-[100px]"
                placeholder="Key points to include…" />
            </div>
          </template>
        </div>

        <div class="flex justify-between mt-6">
          <button class="btn-secondary" @click="step = 0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <button class="btn-primary px-6" :disabled="!canProceedStep2" @click="step = 2">Continue</button>
        </div>
      </div>

      <!-- Step 3: Format -->
      <div v-else-if="step === 2">
        <h2 class="text-2xl font-bold text-[#1d1d1f] tracking-tight mb-1">Configure format</h2>
        <p class="text-[#6e6e73] text-sm mb-7">Customize how your carousel will be generated</p>

        <div class="card p-6 space-y-7">
          <!-- Slides count -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <label class="label mb-0">Number of Slides</label>
              <span class="text-2xl font-bold text-[#0071e3]">{{ slidesCount }}</span>
            </div>
            <input type="range" v-model.number="slidesCount" min="6" max="10" step="1" />
            <div class="flex justify-between text-xs text-[#aeaeb2] mt-1.5 px-0.5">
              <span v-for="n in [6,7,8,9,10]" :key="n"
                :class="slidesCount === n ? 'text-[#0071e3] font-semibold' : ''">{{ n }}</span>
            </div>
          </div>

          <!-- Language -->
          <div>
            <label class="label">Language</label>
            <div class="flex gap-2">
              <button v-for="lang in languages" :key="lang.code"
                class="flex-1 py-2.5 rounded-xl border-2 text-sm font-medium transition-all duration-150"
                :class="language === lang.code
                  ? 'border-[#0071e3] bg-[#0071e3]/5 text-[#0071e3]'
                  : 'border-[#e5e5ea] text-[#6e6e73] hover:border-[#d2d2d7]'"
                @click="language = lang.code">
                {{ lang.label }}
              </button>
            </div>
          </div>

          <!-- Style hint -->
          <div>
            <label class="label">Writing Style <span class="text-[#aeaeb2] normal-case font-normal tracking-normal">— optional</span></label>
            <p class="text-xs text-[#aeaeb2] mb-2">Paste a sample text to match its tone and style</p>
            <textarea v-model="styleHint" class="input min-h-[90px] resize-none"
              placeholder="Paste an example post…" />
          </div>
        </div>

        <!-- Token estimate -->
        <div class="mt-4 p-4 bg-blue-50 border border-blue-100 rounded-2xl flex items-start gap-3">
          <div class="w-7 h-7 bg-blue-100 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
            <svg class="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-blue-800">~{{ estimatedTokens.toLocaleString() }} tokens</p>
            <p class="text-xs text-blue-500 mt-0.5">Estimated usage for this generation</p>
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-100 rounded-2xl text-sm text-red-600">
          {{ error }}
        </div>

        <div class="flex justify-between mt-6">
          <button class="btn-secondary" @click="step = 1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <button class="btn-primary px-6" :disabled="generating" @click="handleCreate">
            <svg v-if="generating" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {{ generating ? 'Creating…' : 'Create & Generate' }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { createCarousel } = useCarousels()
const { startGeneration } = useGeneration()

const step = ref(0)
const sourceType = ref("")
const title = ref("")
const sourceText = ref("")
const videoUrl = ref("")
const videoNotes = ref("")
const links = ref<string[]>([""])
const slidesCount = ref(8)
const language = ref("ru")
const styleHint = ref("")
const generating = ref(false)
const error = ref("")

const steps = ["Source", "Content", "Format"]

const sourceTypes = [
  { key: "text",  icon: "✍️", label: "From Text",   desc: "Paste an article, post, or any text" },
  { key: "video", icon: "🎬", label: "From Video",  desc: "Add a video URL with notes" },
  { key: "links", icon: "🔗", label: "From Links",  desc: "Curate URLs with bullet notes" },
]

const languages = [
  { code: "ru", label: "🇷🇺 Russian" },
  { code: "en", label: "🇬🇧 English" },
  { code: "fr", label: "🇫🇷 French" },
]

const canProceedStep2 = computed(() => {
  if (!title.value.trim()) return false
  if (sourceType.value === "text")  return sourceText.value.trim().length > 10
  if (sourceType.value === "video") return videoUrl.value.trim().length > 5
  if (sourceType.value === "links") return links.value.some((l) => l.trim())
  return false
})

const estimatedTokens = computed(() =>
  200 + Math.min(sourceText.value.length, 2000) + slidesCount.value * 80
)

const buildSourcePayload = () => {
  if (sourceType.value === "text")  return { text: sourceText.value }
  if (sourceType.value === "video") return { video_url: videoUrl.value, notes: videoNotes.value }
  if (sourceType.value === "links") return { links: links.value.filter(Boolean), notes: sourceText.value }
  return {}
}

const handleCreate = async () => {
  error.value = ""
  generating.value = true
  try {
    const carousel = await createCarousel({
      title: title.value,
      source_type: sourceType.value,
      source_payload: buildSourcePayload(),
      format: { slides_count: slidesCount.value, language: language.value as any, style_hint: styleHint.value },
    })
    const gen = await startGeneration(carousel.id)
    router.push(`/carousels/${carousel.id}/edit?gen=${gen.id}`)
  } catch (e: any) {
    error.value = e?.data?.detail || "Something went wrong. Please try again."
    generating.value = false
  }
}
</script>
