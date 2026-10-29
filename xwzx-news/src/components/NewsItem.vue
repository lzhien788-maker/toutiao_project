<template>
  <div class="news-item" @click="goToDetail">
    <div class="news-content">
      <h3 class="news-title">{{ news.title }}</h3>
      <p class="news-desc">{{ news.description }}</p>
      <div class="news-info">
        <span class="news-source">{{ news.author }}</span>
        <span>{{ news.publishTime }}</span>
        <span>{{ news.views }} 阅读</span>
      </div>
    </div>
    <div class="news-image" :class="{ 'is-loaded': imgLoaded }">
      <img
        :src="news.image"
        :alt="news.title"
        loading="lazy"
        @load="imgLoaded = true"
        @error="imgLoaded = true"
      >
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const imgLoaded = ref(false)

const goToDetail = () => {
  router.push(`/news/detail/${props.news.id}`)
}
</script>

<style scoped>
.news-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 14px 13px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
  transition: transform 0.3s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.3s ease;
  overflow: hidden;
  cursor: pointer;
}

.news-item:active {
  transform: scale(0.985);
  box-shadow: var(--app-shadow-1);
}

@media (hover: hover) {
  .news-item:hover {
    transform: translateY(-2px) scale(1.012);
    box-shadow: 0 6px 12px rgba(16, 24, 40, 0.06), 0 16px 32px rgba(22, 119, 255, 0.12);
  }
}

.news-content {
  flex: 1;
  min-width: 0;
}

.news-title {
  margin: 0 0 7px;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--app-text-1);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  transition: color 0.25s ease;
}

.news-item:hover .news-title {
  color: var(--app-primary);
}

.news-desc {
  margin: 0 0 11px;
  font-size: 13px;
  line-height: 1.5;
  color: var(--app-text-3);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--app-text-3);
}

.news-info span + span::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 3px;
  margin: 0 7px;
  border-radius: 50%;
  background-color: #d6d9de;
  vertical-align: middle;
}

.news-source {
  color: var(--app-primary);
  font-weight: 500;
}

.news-image {
  flex-shrink: 0;
  width: 120px;
  height: 80px;
  border-radius: var(--app-radius-sm);
  overflow: hidden;
  background: linear-gradient(135deg, #f0f2f6 0%, #e8ebf1 100%);
}

.news-image img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transform: scale(1.05);
  transition: opacity 0.45s ease, transform 0.6s ease;
}

.news-image.is-loaded img {
  opacity: 1;
  transform: scale(1);
}
</style>
