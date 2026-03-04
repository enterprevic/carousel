export default defineNuxtConfig({
  devtools: { enabled: false },
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt", "@vueuse/nuxt"],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },
  css: ["~/assets/css/main.css"],
  app: {
    head: {
      title: "Carousel Generator",
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
      ],
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&family=Jost:wght@400;700&family=Fredoka:wght@400;700&family=Caveat:wght@400;700&family=Space+Mono:wght@400;700&family=Playfair+Display:wght@400;700&family=Oswald:wght@400;700&family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap",
        },
      ],
    },
  },
})
