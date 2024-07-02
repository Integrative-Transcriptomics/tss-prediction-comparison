import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {    
    // this ensures that the browser opens upon server start
    open: true,
    // this sets a default port to 3000  
    port: 3000, 
    proxy: {
      '/api': {
           target: 'http://127.0.0.1:5000',
           changeOrigin: true,
           secure: false,
       }
      }
},
})
