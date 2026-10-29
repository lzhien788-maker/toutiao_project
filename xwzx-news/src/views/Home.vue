<template>
  <div class="home">
    <van-nav-bar :title="$t('home.title')" fixed />

    <div class="hero-card">
      <span class="hero-orb hero-orb-1"></span>
      <span class="hero-orb hero-orb-2"></span>
      <div class="hero-top">
        <div class="hero-date">{{ todayText }}</div>
        <div class="hero-title">{{ $t('home.title') }}</div>
      </div>
      <div class="hero-stats">
        <div class="hero-stat">
          <span class="hero-stat-num">{{ displayCategories.length }}</span>
          <span class="hero-stat-label">栏目</span>
        </div>
        <span class="hero-stat-divider"></span>
        <div class="hero-stat">
          <span class="hero-stat-num">{{ newsStore.newsList.length }}</span>
          <span class="hero-stat-label">条资讯</span>
        </div>
        <span class="hero-stat-divider"></span>
        <div class="hero-stat">
          <span class="hero-stat-num hero-stat-name">{{ activeCategoryName }}</span>
          <span class="hero-stat-label">当前频道</span>
        </div>
      </div>
    </div>

    <div class="more-options">
      <div class="more-tab" @click="goToCategory">
        {{ $t('home.more') }} <van-icon name="arrow" />
      </div>
    </div>

    <div class="category-tabs">
      <van-tabs
        v-model:active="activeTab"
        sticky
        :offset-top="46"
        swipeable
        animated
        title-active-color="#1677ff"
        title-inactive-color="#5b6069"
      >
        <van-tab
          v-for="(category, index) in displayCategories"
          :key="category.id"
          :title="getCategoryTranslation(category.name)"
          @click="newsStore.changeCategory(category.id)"
        >
          <van-pull-refresh v-model="newsStore.refreshing" @refresh="onRefresh">
            <van-list
              v-model:loading="newsStore.loading"
              :finished="newsStore.finished"
              :finished-text="$t('home.noMore')"
              @load="onLoad"
            >
              <div v-if="newsStore.loading && !newsStore.newsList.length" class="skeleton-wrap">
                <div v-for="n in 4" :key="n" class="skeleton-card">
                  <div class="skeleton-block" style="width: 120px; height: 80px; border-radius: 10px"></div>
                  <div class="skeleton-text">
                    <div class="skeleton-block" style="height: 16px; width: 86%"></div>
                    <div class="skeleton-block" style="height: 16px; width: 58%; margin-top: 10px"></div>
                    <div class="skeleton-block" style="height: 12px; width: 42%; margin-top: 18px"></div>
                  </div>
                </div>
              </div>

              <transition-group name="list-fade" tag="div" class="news-list">
                <news-item
                  v-for="item in newsStore.newsList"
                  :key="item.id"
                  :news="item"
                />
              </transition-group>
            </van-list>
          </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue'
import { useNewsStore } from '../store/modules/news'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import NewsItem from '../components/NewsItem.vue'
import TabBar from '../components/TabBar.vue'

const newsStore = useNewsStore()
const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const activeTab = ref(0)
const tabsTop = ref(0)

watch(
  () => route.query.categoryId,
  (newCategoryId) => {
    if (newCategoryId) {
      const categoryId = parseInt(newCategoryId)
      const filteredCategories = newsStore.categories.filter(category => category.name !== '更多')
      const index = filteredCategories.findIndex(cat => cat.id === categoryId)

      if (index !== -1) {
        activeTab.value = index
        newsStore.changeCategory(categoryId)
      }
    }
  },
  { immediate: true }
)

onMounted(() => {
  newsStore.getCategories().then(() => {
    newsStore.getNewsList()
  })

  setTimeout(updateTabsPosition, 300)

  window.addEventListener('scroll', handleScroll)
})

const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== '更多');
})

const moreCategories = computed(() => {
  return newsStore.categories.filter(category =>
    category.name === '军事' ||
    category.name === '科技' ||
    category.name === '财经'
  );
})

const todayText = computed(() => {
  const now = new Date()
  const week = ['日', '一', '二', '三', '四', '五', '六'][now.getDay()]
  return `${now.getMonth() + 1}月${now.getDate()}日 星期${week}`
})

const activeCategoryName = computed(() => {
  const current = displayCategories.value[activeTab.value]
  return current ? getCategoryTranslation(current.name) : '--'
})

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

const goToCategory = () => {
  router.push('/category')
}

const handleTabClick = (index) => {
  if (displayCategories.value[index].name !== '更多') {
    showDropdown.value = false
    newsStore.changeCategory(displayCategories.value[index].id)
  }
}

const selectMoreCategory = (category) => {
  showDropdown.value = false
  newsStore.changeCategory(category.id)

  const index = newsStore.categories.findIndex(cat => cat.id === category.id)
  if (index !== -1) {
    activeTab.value = index
  }
}

const updateTabsPosition = () => {
  const tabsElement = document.querySelector('.van-tabs__wrap')
  if (tabsElement) {
    tabsTop.value = tabsElement.getBoundingClientRect().top
  }
}

const handleScroll = () => {
  updateTabsPosition()
}

onMounted(() => {
  newsStore.getNewsList()

  setTimeout(updateTabsPosition, 300)

  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

watch(activeTab, (newVal) => {
  const categoryId = newsStore.categories[newVal].id
  newsStore.changeCategory(categoryId)
})

const onRefresh = () => {
  newsStore.getNewsList(true)
}

const onLoad = () => {
  newsStore.getNewsList()
}

const changeCategory = (categoryId) => {
  if (categoryId === 10) {
    goToCategory()
    return
  }

  newsStore.changeCategory(categoryId)
}
</script>

<style scoped>
.home {
  --van-tabs-bottom-bar-color: transparent;
  padding-top: 46px;
  padding-bottom: 60px;
  background-color: var(--app-bg);
  min-height: 100vh;
}

:deep(.van-nav-bar) {
  background-color: var(--app-surface);
  box-shadow: 0 1px 0 rgba(16, 24, 40, 0.04), 0 6px 18px rgba(16, 24, 40, 0.05);
}

:deep(.van-nav-bar__title) {
  font-weight: 700;
  letter-spacing: 0.5px;
}

.hero-card {
  position: relative;
  margin: 12px 12px 14px;
  padding: 18px 18px 16px;
  border-radius: var(--app-radius-lg);
  background: var(--app-gradient);
  box-shadow: var(--app-shadow-primary);
  color: #fff;
  overflow: hidden;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
}

.hero-orb-1 {
  width: 150px;
  height: 150px;
  top: -66px;
  right: -34px;
}

.hero-orb-2 {
  width: 92px;
  height: 92px;
  bottom: -44px;
  right: 66px;
  background: rgba(255, 255, 255, 0.1);
}

.hero-top {
  position: relative;
  z-index: 1;
}

.hero-date {
  font-size: 12px;
  opacity: 0.86;
  letter-spacing: 0.6px;
}

.hero-title {
  margin-top: 4px;
  font-size: 23px;
  font-weight: 700;
  letter-spacing: 2px;
}

.hero-stats {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  margin-top: 16px;
  padding: 11px 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

.hero-stat {
  flex: 1;
  text-align: center;
  min-width: 0;
}

.hero-stat-num {
  display: block;
  font-size: 17px;
  font-weight: 700;
  line-height: 1.3;
}

.hero-stat-name {
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hero-stat-label {
  font-size: 11px;
  opacity: 0.82;
}

.hero-stat-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.28);
}

.category-tabs {
  margin-bottom: 10px;
  position: relative;
}

:deep(.van-tabs__wrap) {
  background-color: var(--app-surface);
  border-bottom: 1px solid var(--app-line);
}

:deep(.van-tabs__nav) {
  padding-right: 70px;
}

:deep(.van-tab) {
  font-size: 14px;
  transition: color 0.26s ease;
}

:deep(.van-tab--active) {
  font-weight: 700;
}

:deep(.van-tab__text) {
  padding: 5px 11px;
  border-radius: 999px;
  transition: background-color 0.26s ease, transform 0.26s ease;
}

:deep(.van-tab--active) .van-tab__text {
  background-color: var(--app-primary-soft);
  transform: translateY(-1px);
}

.more-options {
  position: fixed;
  right: max(0px, calc((100vw - 750px) / 2));
  top: v-bind('tabsTop + "px"');
  height: 44px;
  display: flex;
  align-items: center;
  background-color: var(--app-surface);
  border-left: 1px solid var(--app-line);
  box-shadow: -4px 0 14px rgba(16, 24, 40, 0.05);
  z-index: 1000;
}

.more-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  cursor: pointer;
  color: var(--app-primary);
  font-size: 13px;
  font-weight: 600;
  height: 100%;
  padding: 0 12px;
  transition: opacity 0.2s ease;
}

.more-tab:active {
  opacity: 0.6;
}

.skeleton-wrap {
  padding: 12px 12px 0;
}

.news-list {
  position: relative;
  padding: 12px 12px 4px;
}

:deep(.van-list__loading) {
  justify-content: center;
  padding: 14px 0;
  color: var(--app-text-3);
  font-size: 13px;
}

:deep(.van-list__loading-icon) {
  color: var(--app-primary);
}

:deep(.van-list__finished-text) {
  padding: 16px 0 20px;
  color: var(--app-text-3);
  font-size: 12px;
  text-align: center;
}

:deep(.van-pull-refresh__head) {
  color: var(--app-text-3);
  font-size: 12px;
}
</style>
