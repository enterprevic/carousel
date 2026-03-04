export type SourceType = "text" | "video" | "links"
export type CarouselStatus = "draft" | "generating" | "ready" | "failed"
export type GenerationStatus = "queued" | "running" | "done" | "failed"
export type ExportStatus = "queued" | "running" | "done" | "failed"
export type Template = "bright" | "classic" | "comic" | "elegant" | "minimal" | "notes" | "powerful"
export type Language = "ru" | "en" | "fr"

export interface CarouselFormat {
  slides_count: number
  language: Language
  style_hint: string
}

export type FontChoice = "system" | "playfair" | "oswald" | "montserrat" | "opensans" | "lato" | "merriweather" | "georgia"
export type AspectRatio = "4:5" | "9:16" | "1:1"
export type Pattern = "none" | "dots1" | "dots2" | "dots3" | "grid" | "lines" | "cells" | "blobs"

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
  title_font: FontChoice
  body_font: FontChoice
  aspect_ratio: AspectRatio
  accent_color: string | null
  pattern: Pattern
  pattern_color: string
  pattern_opacity: number
  title_highlight: string | null
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

export interface SlideOverrides {
  // Background
  bg_color?: string | null
  bg_image_url?: string | null
  darkening?: number | null
  // Style
  template?: Template | null
  accent_color?: string | null
  title_highlight?: string | null
  align_h?: "left" | "center" | "right" | null
  align_v?: "top" | "center" | "bottom" | null
  // Pattern
  pattern?: Pattern | null
  pattern_color?: string | null
  pattern_opacity?: number | null
  // Layout
  padding?: number | null
  show_header?: boolean | null
  header_text?: string | null
  show_footer?: boolean | null
  footer_text?: string | null
}

export interface Slide {
  id: string
  carousel_id: string
  order: number
  title: string
  body: string
  footer_cta: string | null
  overrides: SlideOverrides
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
  error: string | null
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
  title_font: "system",
  body_font: "system",
  aspect_ratio: "4:5",
  accent_color: null,
  pattern: "none",
  pattern_color: "#000000",
  pattern_opacity: 0.06,
  title_highlight: null,
}

export const FONT_FAMILIES: Record<string, string> = {
  system: "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif",
  playfair: "'Playfair Display', Georgia, serif",
  oswald: "'Oswald', 'Arial Narrow', sans-serif",
  montserrat: "'Montserrat', 'Helvetica Neue', sans-serif",
  opensans: "'Open Sans', Helvetica, sans-serif",
  lato: "'Lato', 'Helvetica Neue', sans-serif",
  merriweather: "'Merriweather', Georgia, serif",
  georgia: "Georgia, 'Times New Roman', serif",
}
