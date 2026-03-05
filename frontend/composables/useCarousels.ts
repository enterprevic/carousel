import type { Carousel, CarouselFormat } from "~/types"

export const useCarousels = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase
  const { authHeaders } = useAuth()

  const fetchCarousels = async (params?: { status?: string; lang?: string }): Promise<Carousel[]> => {
    const q = new URLSearchParams()
    if (params?.status) q.set("status", params.status)
    if (params?.lang) q.set("lang", params.lang)
    const url = `${base}/carousels${q.toString() ? "?" + q.toString() : ""}`
    return await $fetch<Carousel[]>(url, { headers: authHeaders() })
  }

  const fetchCarousel = async (id: string): Promise<Carousel> => {
    return await $fetch<Carousel>(`${base}/carousels/${id}`, { headers: authHeaders() })
  }

  const createCarousel = async (body: {
    title: string
    source_type: string
    source_payload: Record<string, any>
    format: Partial<CarouselFormat>
  }): Promise<Carousel> => {
    return await $fetch<Carousel>(`${base}/carousels`, { method: "POST", body, headers: authHeaders() })
  }

  const updateCarousel = async (id: string, body: Partial<{ title: string; format: CarouselFormat }>) => {
    return await $fetch<Carousel>(`${base}/carousels/${id}`, { method: "PATCH", body, headers: authHeaders() })
  }

  const updateDesign = async (id: string, design: Record<string, any>) => {
    return await $fetch<Carousel>(`${base}/carousels/${id}/design`, { method: "PATCH", body: design, headers: authHeaders() })
  }

  const fetchGenerations = async (carouselId: string) => {
    return await $fetch<import("~/types").Generation[]>(`${base}/carousels/${carouselId}/generations`, { headers: authHeaders() })
  }

  const deleteCarousel = async (id: string): Promise<void> => {
    await $fetch(`${base}/carousels/${id}`, { method: "DELETE", headers: authHeaders() })
  }

  const deleteSlide = async (carouselId: string, slideId: string): Promise<void> => {
    await $fetch(`${base}/carousels/${carouselId}/slides/${slideId}`, { method: "DELETE", headers: authHeaders() })
  }

  const moveSlide = async (carouselId: string, slideId: string, newOrder: number): Promise<import("~/types").Slide[]> => {
    return await $fetch(`${base}/carousels/${carouselId}/slides/${slideId}/order`, {
      method: "PATCH", body: { new_order: newOrder }, headers: authHeaders()
    })
  }

  return { fetchCarousels, fetchCarousel, createCarousel, updateCarousel, updateDesign, fetchGenerations, deleteCarousel, deleteSlide, moveSlide }
}
