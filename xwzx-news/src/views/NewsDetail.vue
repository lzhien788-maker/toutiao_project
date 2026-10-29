<template>
  <div class="news-detail">
    <van-nav-bar
      title="新闻详情"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />

    <div class="reading-progress">
      <span class="reading-progress-bar" :style="{ width: scrollProgress + '%' }"></span>
    </div>

    <div class="detail-content" v-if="newsStore.newsDetail.id">
      <div class="title-container">
        <h1 class="title">{{ newsStore.newsDetail.title }}</h1>
        <van-button
          class="favorite-btn"
          :icon="isFavorite ? 'star' : 'star-o'"
          :class="{ 'is-favorite': isFavorite }"
          @click="toggleFavorite"
        />
      </div>

      <div class="info">
        <span class="info-author">{{ newsStore.newsDetail.author }}</span>
        <span>{{ newsStore.newsDetail.publishTime }}</span>
        <span>{{ newsStore.newsDetail.views }} 阅读</span>
      </div>

      <div class="cover" v-if="newsStore.newsDetail.image">
        <img :src="newsStore.newsDetail.image" :alt="newsStore.newsDetail.title">
      </div>

      <div class="content">
        <p v-for="(paragraph, index) in contentParagraphs" :key="index">
          {{ paragraph }}
        </p>
      </div>

      <div class="article-footer">
        <span class="footer-line"></span>
        <span class="footer-text">— 感谢阅读 · 往期回顾 —</span>
        <span class="footer-line"></span>
      </div>

      <div class="related-news" v-if="newsStore.newsDetail.relatedNews?.length">
        <div class="section-title">相关推荐</div>
        <div class="related-list">
          <div
            class="related-item"
            v-for="item in newsStore.newsDetail.relatedNews"
            :key="item.id"
            @click="goToRelatedNews(item.id)"
          >
            <div class="related-image">
              <img :src="item.image" :alt="item.title" loading="lazy">
            </div>
            <div class="related-info">
              <div class="related-title">{{ item.title }}</div>
              <div class="related-meta">点击查看详情</div>
            </div>
            <van-icon name="arrow" class="related-arrow" />
          </div>
        </div>
      </div>
    </div>

    <div class="detail-loading" v-else>
      <div class="skeleton-block" style="height: 26px; width: 80%"></div>
      <div class="skeleton-block" style="height: 26px; width: 55%; margin-top: 12px"></div>
      <div class="skeleton-block" style="height: 12px; width: 40%; margin-top: 18px"></div>
      <div class="skeleton-block" style="height: 170px; width: 100%; margin-top: 22px; border-radius: 16px"></div>
      <div class="skeleton-block" style="height: 15px; width: 100%; margin-top: 24px"></div>
      <div class="skeleton-block" style="height: 15px; width: 96%; margin-top: 12px"></div>
      <div class="skeleton-block" style="height: 15px; width: 88%; margin-top: 12px"></div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNewsStore } from '../store/modules/news'
import { useHistoryStore } from '../store/modules/history'
import { useFavoriteStore } from '../store/modules/favorite'
import { useUserStore } from '../store/user'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()
const historyStore = useHistoryStore()
const favoriteStore = useFavoriteStore()
const userStore = useUserStore()

const newsId = computed(() => Number(route.params.id))

const scrollProgress = ref(0)

const contentParagraphs = computed(() => {
  if (!newsStore.newsDetail.content) return []
  return newsStore.newsDetail.content.split('\n\n').filter(p => p.trim())
})

const onClickLeft = () => {
  router.back()
}

const goToRelatedNews = (id) => {
  router.push(`/news/detail/${id}`)
}

const isFavorite = computed(() => {
  return favoriteStore.isFavorite(newsId.value)
})

const toggleFavorite = async () => {
  if (!userStore.getLoginStatus) {
    showToast({
      message: '请先登录后再收藏',
      position: 'bottom',
    })
    router.push('/login')
    return
  }

  const status = await favoriteStore.toggleFavorite(newsStore.newsDetail)

  if (status === true) {
    showToast({
      message: '已添加到收藏',
      position: 'bottom',
    })
  } else if (status === false) {
    showToast({
      message: '已取消收藏',
      position: 'bottom',
    })
  } else {
    showToast({
      message: '操作失败，请稍后重试',
      position: 'bottom',
    })
  }
}

const updateProgress = () => {
  const doc = document.documentElement
  const scrollable = doc.scrollHeight - doc.clientHeight
  scrollProgress.value = scrollable > 0 ? Math.min(100, (doc.scrollTop / scrollable) * 100) : 0
}

onMounted(async () => {
  window.addEventListener('scroll', updateProgress, { passive: true })
  updateProgress()

  await newsStore.getNewsDetail(newsId.value)

  if (newsStore.newsDetail.id) {
    if (userStore.getLoginStatus) {
      try {
        const result = await historyStore.addHistoryApi(newsStore.newsDetail.id);
        console.log('记录浏览历史API结果:', result);
      } catch (error) {
        console.error('记录浏览历史API失败:', error);
      }
    }
  }

  favoriteStore.loadFavorites()

  if (userStore.getLoginStatus && newsStore.newsDetail.id) {
    const result = await favoriteStore.checkFavoriteStatusApi(newsStore.newsDetail.id)
    if (result.success && !result.isLocal) {
      if (result.isFavorite && !favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.addFavorite(newsStore.newsDetail)
      } else if (!result.isFavorite && favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.removeFavorite(newsStore.newsDetail.id)
      }
    }
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', updateProgress)
})
</script>

<style scoped>
.news-detail {
  padding-top: 46px;
  padding-bottom: 40px;
  background-color: var(--app-bg);
  min-height: 100vh;
}

:deep(.van-nav-bar) {
  background-color: var(--app-surface);
  box-shadow: 0 1px 0 rgba(16, 24, 40, 0.04), 0 6px 18px rgba(16, 24, 40, 0.05);
}

.reading-progress {
  position: fixed;
  top: 45px;
  left: 0;
  right: 0;
  height: 2px;
  z-index: 1000;
  pointer-events: none;
}

.reading-progress-bar {
  display: block;
  height: 100%;
  background: var(--app-gradient);
  transition: width 0.1s linear;
}

.detail-content {
  padding: 18px 16px 0;
}

.title-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.title {
  flex: 1;
  font-size: 23px;
  font-weight: 700;
  line-height: 1.42;
  color: var(--app-text-1);
  margin: 0;
  letter-spacing: 0.2px;
}

.favorite-btn {
  flex-shrink: 0;
  margin-top: 2px;
  padding: 0;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background-color: var(--app-surface);
  border: 1px solid var(--app-line);
  box-shadow: var(--app-shadow-1);
  color: var(--app-text-3);
  transition: transform 0.25s ease, color 0.25s ease, background-color 0.25s ease;
}

.favorite-btn:active {
  transform: scale(0.9);
}

.favorite-btn.is-favorite {
  color: #ff9500;
  background-color: rgba(255, 149, 0, 0.1);
  border-color: rgba(255, 149, 0, 0.28);
}

.info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px 0;
  font-size: 12px;
  color: var(--app-text-3);
  margin-bottom: 18px;
}

.info span + span::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 3px;
  margin: 0 10px;
  border-radius: 50%;
  background-color: #d6d9de;
  vertical-align: middle;
}

.info-author {
  color: var(--app-primary);
  font-weight: 600;
}

.cover {
  margin-bottom: 22px;
}

.cover img {
  display: block;
  width: 100%;
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
}

.content {
  font-size: 17px;
  line-height: 1.92;
  color: #2b2f36;
  letter-spacing: 0.2px;
}

.content p {
  margin-bottom: 18px;
  text-align: justify;
}

.article-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 28px 0 6px;
}

.footer-line {
  width: 40px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--app-line));
}

.footer-line:last-child {
  background: linear-gradient(90deg, var(--app-line), transparent);
}

.footer-text {
  font-size: 12px;
  color: var(--app-text-3);
  letter-spacing: 1px;
}

.related-news {
  margin-top: 30px;
}

.related-list {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.related-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
  transition: transform 0.28s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.28s ease;
  cursor: pointer;
}

.related-item:active {
  transform: scale(0.985);
}

@media (hover: hover) {
  .related-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--app-shadow-3);
  }
}

.related-image {
  width: 96px;
  height: 64px;
  flex-shrink: 0;
  border-radius: var(--app-radius-sm);
  overflow: hidden;
  background: linear-gradient(135deg, #f0f2f6 0%, #e8ebf1 100%);
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.related-info {
  flex: 1;
  min-width: 0;
}

.related-title {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--app-text-1);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.related-meta {
  margin-top: 6px;
  font-size: 12px;
  color: var(--app-text-3);
}

.related-arrow {
  flex-shrink: 0;
  color: #cfd4dc;
  font-size: 15px;
}

.detail-loading {
  padding: 22px 16px;
}
</style>
