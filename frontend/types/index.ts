export type SourceType = "text" | "video" | "links"
export type CarouselStatus = "draft" | "generating" | "ready" | "failed"
export type GenerationStatus = "queued" | "running" | "done" | "failed"
export type ExportStatus = "queued" | "running" | "done" | "failed"
export type Template = "classic" | "bold" | "minimal"
export type Language = "ru" | "en" | "fr"

export interface CarouselFormat {
  slides_count: number
  language: Language
  style_hint: string
}

export interface CarouselDesign {
  template: Template
  bg_color: string
  bg_image_url: string | null
  darkening: number
  padding: number
  align_h: "left" | "center" | "right"
  align_v: "top" | "center" | "bottom"
  show_header: boolean
  header_text: string
  show_footer: boolean
  footer_text: string
}

export interface Carousel {
  id: string
  title: string
  source_type: SourceType
  source_payload: Record<string, any>
  format: CarouselFormat
  design: CarouselDesign
  status: CarouselStatus
  created_at: string
  updated_at: string
}

export interface Slide {
  id: string
  carousel_id: string
  order: number
  title: string
  body: string
  footer_cta: string | null
  created_at: string
  updated_at: string
}

export interface Generation {
  id: string
  carousel_id: string
  status: GenerationStatus
  tokens_used: number | null
  error: string | null
  estimated_tokens?: number
  created_at: string
  updated_at: string
}

export interface Export {
  id: string
  carousel_id: string
  status: ExportStatus
  file_url: string | null
  created_at: string
}

export const DEFAULT_DESIGN: CarouselDesign = {
  template: "classic",
  bg_color: "#ffffff",
  bg_image_url: null,
  darkening: 0,
  padding: 40,
  align_h: "center",
  align_v: "center",
  show_header: false,
  header_text: "",
  show_footer: false,
  footer_text: "",
}
