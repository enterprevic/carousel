import { defineStore } from "pinia"
import type { Carousel, Slide, CarouselDesign } from "~/types"

export const useEditorStore = defineStore("editor", {
  state: () => ({
    carousel: null as Carousel | null,
    slides: [] as Slide[],
    activeSlideIndex: 0,
    saving: false,
  }),
  getters: {
    activeSlide: (state): Slide | null => state.slides[state.activeSlideIndex] ?? null,
    design: (state): CarouselDesign | null => state.carousel?.design ?? null,
  },
  actions: {
    setCarousel(carousel: Carousel) {
      this.carousel = carousel
    },
    setSlides(slides: Slide[]) {
      this.slides = slides
      this.activeSlideIndex = 0
    },
    setActiveSlide(index: number) {
      this.activeSlideIndex = index
    },
    updateSlideLocally(slideId: string, patch: Partial<Slide>) {
      const idx = this.slides.findIndex((s) => s.id === slideId)
      if (idx !== -1) {
        this.slides[idx] = { ...this.slides[idx], ...patch }
      }
    },
    updateDesignLocally(design: CarouselDesign) {
      if (this.carousel) {
        this.carousel = { ...this.carousel, design }
      }
    },
  },
})
