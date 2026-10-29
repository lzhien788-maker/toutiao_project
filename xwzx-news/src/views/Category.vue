<template>
  <div class="category">
    <van-nav-bar
      :title="$t('common.allCategories')"
      :left-text="$t('common.back')"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />

    <div class="category-hero">
      <span class="hero-orb hero-orb-1"></span>
      <span class="hero-orb hero-orb-2"></span>
      <div class="hero-label">EXPLORE</div>
      <div class="hero-title">发现更多精彩栏目</div>
      <div class="hero-desc">共 {{ displayCategories.length }} 个频道，按你的兴趣随时切换</div>
    </div>

    <div class="category-panel">
      <div class="panel-head">
        <div class="section-title">
          全部栏目
        </div>
        <span class="section-desc">点击进入对应频道</span>
      </div>

      <div class="category-grid">
        <div
          class="category-card"
          v-for="(category, index) in displayCategories"
          :key="category.id"
          :style="{ animationDelay: index * 40 + 'ms' }"
          @click="goToCategoryNews(category.id)"
        >
          <div class="category-icon" :style="{ background: getCategoryGradient(category.name) }">
            <van-icon :name="getCategoryIcon(category.name)" />
          </div>
          <div class="category-name">{{ getCategoryTranslation(category.name) }}</div>
          <div class="category-arrow">
            <van-icon name="arrow" />
          </div>
        </div>
      </div>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { useNewsStore } from '../store/modules/news'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import TabBar from '../components/TabBar.vue'
import { computed } from 'vue'

const newsStore = useNewsStore()
const router = useRouter()
const { t } = useI18n()

// 计算属性：显示的分类（只显示非"更多"分类）
const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== '更多');
})

// 返回上一页
const onClickLeft = () => {
  router.back()
}

// 跳转到对应分类的新闻列表
const goToCategoryNews = (categoryId) => {
  // 先切换分类
  newsStore.changeCategory(categoryId)

  // 使用路由参数传递分类ID
  router.push({
    path: '/home',
    query: { categoryId: categoryId }
  })
}

// 获取分类名称的翻译
const getCategoryTranslation = (categoryName) => {
  const categoryMap = {
    '头条': 'headline',
    '社会': 'society',
    '国内': 'domestic',
    '国际': 'international',
    '娱乐': 'entertainment',
    '体育': 'sports',
    '军事': 'military',
    '科技': 'technology',
    '财经': 'finance',
    '更多': 'more'
  };

  const key = categoryMap[categoryName];
  return key ? t(`home.categories.${key}`) : categoryName;
}

// 每个栏目对应一套图标与渐变配色，保证视觉有节奏感
const categoryStyleMap = {
  '头条': { icon: 'fire-o', gradient: 'linear-gradient(135deg, #ff6a3d 0%, #ff3b30 100%)' },
  '社会': { icon: 'friends-o', gradient: 'linear-gradient(135deg, #4aa8ff 0%, #1677ff 100%)' },
  '国内': { icon: 'location-o', gradient: 'linear-gradient(135deg, #38c793 0%, #16a06a 100%)' },
  '国际': { icon: 'global-o', gradient: 'linear-gradient(135deg, #8b6cf0 0%, #6a4bd8 100%)' },
  '娱乐': { icon: 'star-o', gradient: 'linear-gradient(135deg, #ff6bb0 0%, #f0428a 100%)' },
  '体育': { icon: 'medal-o', gradient: 'linear-gradient(135deg, #ffc53d 0%, #f5a300 100%)' },
  '军事': { icon: 'shield-o', gradient: 'linear-gradient(135deg, #5f6b7a 0%, #3d4757 100%)' },
  '科技': { icon: 'bulb-o', gradient: 'linear-gradient(135deg, #22c1c3 0%, #0f9aa8 100%)' },
  '财经': { icon: 'bar-chart-o', gradient: 'linear-gradient(135deg, #22a06b 0%, #0f7a50 100%)' }
}

const getCategoryIcon = (categoryName) => {
  return categoryStyleMap[categoryName]?.icon || 'newspaper-o'
}

const getCategoryGradient = (categoryName) => {
  return categoryStyleMap[categoryName]?.gradient || 'linear-gradient(135deg, #6bb4ff 0%, #3d8cff 100%)'
}
</script>

<style scoped>
.category {
  padding-bottom: 60px;
  background-color: var(--app-bg);
  min-height: 100vh;
}

:deep(.van-nav-bar) {
  background-color: transparent;
  box-shadow: none;
}

:deep(.van-nav-bar__title),
:deep(.van-nav-bar__left) {
  color: #fff;
}

:deep(.van-nav-bar__left .van-icon) {
  color: #fff;
}

.category-hero {
  position: relative;
  padding: 62px 20px 48px;
  background: var(--app-header-gradient);
  border-radius: 0 0 28px 28px;
  box-shadow: var(--app-shadow-primary);
  overflow: hidden;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.16);
}

.hero-orb-1 {
  width: 180px;
  height: 180px;
  top: -70px;
  right: -40px;
}

.hero-orb-2 {
  width: 110px;
  height: 110px;
  bottom: -46px;
  left: 22px;
  background: rgba(255, 255, 255, 0.1);
}

.hero-label {
  font-size: 11px;
  letter-spacing: 4px;
  color: rgba(255, 255, 255, 0.72);
  font-weight: 600;
}

.hero-title {
  margin-top: 8px;
  font-size: 25px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}

.hero-desc {
  margin-top: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.82);
}

.category-panel {
  position: relative;
  margin: -32px 12px 0;
  padding: 18px 12px 14px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius-lg);
  box-shadow: var(--app-shadow-3);
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 4px 14px;
}

.panel-head .section-desc {
  font-weight: 400;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.category-card {
  position: relative;
  padding: 18px 10px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
  animation: category-in 0.45s cubic-bezier(0.22, 0.61, 0.36, 1) both;
  transition: transform 0.28s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.28s ease;
  overflow: hidden;
}

.category-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--app-radius);
  border: 1px solid transparent;
  transition: border-color 0.28s ease;
}

.category-card:active {
  transform: scale(0.97);
}

@media (hover: hover) {
  .category-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--app-shadow-3);
  }

  .category-card:hover::after {
    border-color: rgba(22, 119, 255, 0.28);
  }
}

@keyframes category-in {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.category-icon {
  width: 52px;
  height: 52px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  color: #fff;
  box-shadow: 0 8px 18px rgba(16, 24, 40, 0.16);
}

.category-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--app-text-1);
  text-align: center;
}

.category-arrow {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 12px;
  color: var(--app-text-3);
  opacity: 0;
  transform: translateX(-4px);
  transition: all 0.28s ease;
}

@media (hover: hover) {
  .category-card:hover .category-arrow {
    opacity: 1;
    transform: translateX(0);
    color: var(--app-primary);
  }
}
</style>
