import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  // 关键配置
  optimizeDeps: {
    exclude: ['vant']
  },
  resolve: {
    alias: {
    }
  }
})
