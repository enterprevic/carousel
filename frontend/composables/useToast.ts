const toasts = ref<{ id: number; message: string; type: 'info' | 'error' | 'warning' }[]>([])
let nextId = 0

export const useToast = () => {
  const show = (message: string, type: 'info' | 'error' | 'warning' = 'info', duration = 4000) => {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      const i = toasts.value.findIndex((t) => t.id === id)
      if (i !== -1) toasts.value.splice(i, 1)
    }, duration)
  }

  return { toasts, show }
}
