export const useAuth = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  const getToken = (): string | null =>
    import.meta.client ? localStorage.getItem("auth_token") : null

  const getUsername = (): string =>
    (import.meta.client ? localStorage.getItem("auth_username") : null) ?? ""

  const setToken = (t: string) => localStorage.setItem("auth_token", t)
  const clearToken = () => {
    localStorage.removeItem("auth_token")
    localStorage.removeItem("auth_username")
  }

  const login = async (username: string, password: string): Promise<void> => {
    const { token } = await $fetch<{ token: string }>(`${base}/auth/login`, {
      method: "POST",
      body: { username, password },
    })
    setToken(token)
    localStorage.setItem("auth_username", username)
  }

  const register = async (username: string, password: string): Promise<void> => {
    const { token } = await $fetch<{ token: string }>(`${base}/auth/register`, {
      method: "POST",
      body: { username, password },
    })
    setToken(token)
    localStorage.setItem("auth_username", username)
  }

  const logout = () => {
    clearToken()
    navigateTo("/")
  }

  const authHeaders = (): Record<string, string> => {
    const t = getToken()
    return t ? { Authorization: `Bearer ${t}` } : {}
  }

  return { login, register, logout, getToken, getUsername, setToken, clearToken, authHeaders }
}
