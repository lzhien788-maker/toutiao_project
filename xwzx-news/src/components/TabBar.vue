<template>
  <van-tabbar v-model="active" route class="app-tabbar" safe-area-inset-bottom>
    <van-tabbar-item to="/home" icon="home-o">{{ $t('nav.home') }}</van-tabbar-item>
    <van-tabbar-item to="/aichat" icon="chat-o">{{ $t('nav.aiChat') }}</van-tabbar-item>
    <van-tabbar-item to="/my" icon="user-o">{{ $t('nav.my') }}</van-tabbar-item>
  </van-tabbar>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

// 根据当前路由路径设置激活的标签
const setActiveTab = () => {
  const path = route.path
  if (path.includes('/home')) {
    active.value = 0
  } else if (path.includes('/aichat')) {
    active.value = 1
  } else if (path.includes('/my')) {
    active.value = 2
  }
}

// 初始化时设置激活标签
setActiveTab()
</script>

<style scoped>
.app-tabbar {
  background-color: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 -2px 16px rgba(16, 24, 40, 0.07);
}

.app-tabbar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(16, 24, 40, 0.07) 50%, transparent 100%);
}

:deep(.van-tabbar-item) {
  transition: transform 0.24s ease;
}

:deep(.van-tabbar-item--active) {
  transform: translateY(-1px);
}

:deep(.van-tabbar-item--active .van-tabbar-item__icon) {
  color: var(--app-primary);
}

:deep(.van-tabbar-item__icon) {
  font-size: 22px;
  margin-bottom: 3px;
  transition: transform 0.24s cubic-bezier(0.22, 0.61, 0.36, 1), color 0.24s ease;
}

:deep(.van-tabbar-item--active .van-tabbar-item__icon) {
  transform: translateY(-1px) scale(1.08);
}

:deep(.van-tabbar-item__text) {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.3px;
}

:deep(.van-tabbar-item--active .van-tabbar-item__text) {
  font-weight: 700;
}
</style>
