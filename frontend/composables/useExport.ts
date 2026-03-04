import type { Export } from "~/types"

export const useExport = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  const startExport = async (carouselId: string): Promise<Export> => {
    return await $fetch<Export>(`${base}/exports`, {
      method: "POST",
      body: { carousel_id: carouselId },
    })
  }

  const getExport = async (id: string): Promise<Export> => {
    return await $fetch<Export>(`${base}/exports/${id}`)
  }

  const pollExport = (
    id: string,
    onDone: (exp: Export) => void,
    onFail: () => void,
  ) => {
    const interval = setInterval(async () => {
      try {
        const exp = await getExport(id)
        if (exp.status === "done") {
          clearInterval(interval)
          onDone(exp)
        } else if (exp.status === "failed") {
          clearInterval(interval)
          onFail()
        }
      } catch {
        clearInterval(interval)
      }
    }, 2000)
    return () => clearInterval(interval)
  }

  return { startExport, getExport, pollExport }
}
