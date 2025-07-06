import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy API requests to the backend server during development
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // The FastAPI backend
        changeOrigin: true,
      },
    },
  },
})