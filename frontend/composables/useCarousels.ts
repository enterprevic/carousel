import type { Carousel, CarouselFormat } from "~/types"

export const useCarousels = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  const fetchCarousels = async (params?: { status?: string; lang?: string }): Promise<Carousel[]> => {
    const q = new URLSearchParams()
    if (params?.status) q.set("status", params.status)
    if (params?.lang) q.set("lang", params.lang)
    const url = `${base}/carousels${q.toString() ? "?" + q.toString() : ""}`
    return await $fetch<Carousel[]>(url)
  }

  const fetchCarousel = async (id: string): Promise<Carousel> => {
    return await $fetch<Carousel>(`${base}/carousels/${id}`)
  }

  const createCarousel = async (body: {
    title: string
    source_type: string
    source_payload: Record<string, any>
    format: Partial<CarouselFormat>
  }): Promise<Carousel> => {
    return await $fetch<Carousel>(`${base}/carousels`, { method: "POST", body })
  }

  const updateCarousel = async (id: string, body: Partial<{ title: string; format: CarouselFormat }>) => {
    return await $fetch<Carousel>(`${base}/carousels/${id}`, { method: "PATCH", body })
  }

  const updateDesign = async (id: string, design: Record<string, any>) => {
    return await $fetch<Carousel>(`${base}/carousels/${id}/design`, { method: "PATCH", body: design })
  }

  return { fetchCarousels, fetchCarousel, createCarousel, updateCarousel, updateDesign }
}
