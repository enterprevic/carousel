export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: false },
  modules: ["@nuxtjs/tailwindcss"],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },
  css: ["~/assets/css/main.css"],
  app: {
    head: {
      title: "trendsee",
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
      ],
      link: [
        { rel: "icon", type: "image/png", href: "/visible.png", sizes: "32x32" },
        { rel: "shortcut icon", href: "/visible.png" },
        { rel: "apple-touch-icon", href: "/visible.png" },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Unbounded:wght@600&family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;700&family=Roboto+Condensed:wght@400;700&family=Jost:wght@400;700&family=Caveat:wght@400;700&family=Source+Sans+3:wght@400;600;700&family=Fredoka:wght@400;700&family=Space+Mono:wght@400;700&family=Playfair+Display:wght@400;700&family=Oswald:wght@400;700&family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap",
        },
      ],
    },
  },
})
