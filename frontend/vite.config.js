import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\//, ""),
      },
      "/auth": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\//, ""),
      },
      "/env": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\//, ""),
      },
    },
  },
  base: "./",
  build: {
    emptyOutDir: true,
    assetDir: "static/products/",
    rollupOptions: {
      output: {
        entryFileNames: "static/products/[name].js",
        chunkFileNames: "static/products/[name].js",
        assetFileNames: "static/products/assets/[name][extname]",
      },
    },
  },
})
