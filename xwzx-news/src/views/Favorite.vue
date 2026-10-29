<template>
  <div class="favorite-container">
    <van-nav-bar
      title="我的收藏"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
      right-text="清空"
      @click-right="onClickClear"
      fixed
    />

    <div class="favorite-summary" v-if="favoriteStore.getFavorites.length">
      <div class="summary-icon"><van-icon name="like" /></div>
      <div class="summary-text">
        <div class="summary-num">{{ favoriteStore.getFavorites.length }}</div>
        <div class="summary-label">篇收藏好文</div>
      </div>
      <div class="summary-tip">点击卡片查看详情</div>
    </div>

    <div class="favorite-list" v-if="favoriteStore.getFavorites.length">
      <div class="favorite-item" v-for="item in favoriteStore.getFavorites" :key="item.id">
        <van-cell @click="goToNewsDetail(item.id)" :border="false" class="favorite-cell">
          <template #title>
            <div class="favorite-card">
              <div class="favorite-main">
                <div class="news-title">{{ item.title }}</div>
                <div class="news-meta">
                  <span>{{ item.author }}</span>
                  <span>{{ item.publishTime }}</span>
                </div>
                <div class="news-favtime">
                  <van-icon name="star-o" />
                  <span>收藏于 {{ item.favoriteTime }}</span>
                </div>
              </div>
              <div class="news-image" v-if="item.image">
                <img :src="item.image" :alt="item.title" loading="lazy">
              </div>
            </div>
          </template>
        </van-cell>
        <van-button
          class="delete-btn"
          type="danger"
          size="mini"
          icon="cross"
          @click="confirmDelete(item.id)"
        ></van-button>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon"><van-icon name="star-o" /></div>
      <div class="empty-title">暂无收藏内容</div>
      <div class="empty-desc">看到喜欢的文章点个收藏，方便随时回看</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useFavoriteStore } from '../store/modules/favorite';
import { showDialog } from 'vant';

const router = useRouter();
const favoriteStore = useFavoriteStore();

// 返回上一页
const onClickLeft = () => {
  router.back();
};

// 跳转到新闻详情
const goToNewsDetail = (id) => {
  router.push(`/news/detail/${id}`);
};

// 删除单条收藏
const removeFavorite = async (id) => {
  const result = await favoriteStore.removeFavoriteApi(id);
  if (result.success) {
    // API请求成功后，更新本地收藏列表
    favoriteStore.removeFavorite(id);
  }
};

// 确认删除
const confirmDelete = (id) => {
  showDialog({
    title: '提示',
    message: '确定要删除这条收藏吗？',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      removeFavorite(id);
    }
  });
};

// 清空收藏
const onClickClear = async () => {
  showDialog({
    title: '提示',
    message: '确定要清空所有收藏吗？',
    showCancelButton: true,
  }).then(async (action) => {
    if (action === 'confirm') {
      const result = await favoriteStore.clearFavoritesApi();
      if (!result || !result.success) {
        // 如果API请求失败，回退到本地清空
        // favoriteStore.clearFavorites();
        console.log('清空收藏列表');
      }
    }
  });
};

// 组件挂载时加载收藏数据
onMounted(async () => {
  // 使用API请求获取收藏列表
  try {

    const result = await favoriteStore.getFavoriteListApi();
    if (!result || !result.success) {
      // 如果API请求失败，回退到本地存储
      // favoriteStore.loadFavorites();
      console.log('从本地存储加载收藏列表');
    }
  } catch (error) {
    favoriteStore.loadFavorites();
  }
});
</script>

<style scoped>
.favorite-container {
  padding-top: 46px;
  padding-bottom: 30px;
  background-color: var(--app-bg);
  min-height: 100vh;
}

:deep(.van-nav-bar) {
  background-color: var(--app-surface);
  box-shadow: 0 1px 0 rgba(16, 24, 40, 0.04), 0 6px 18px rgba(16, 24, 40, 0.05);
}

:deep(.van-nav-bar__right) {
  color: var(--app-primary);
}

.favorite-summary {
  margin: 14px 12px 0;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: var(--app-radius);
  background: var(--app-gradient-soft);
  border: 1px solid rgba(22, 119, 255, 0.16);
}

.summary-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #fff;
  background: var(--app-gradient);
  box-shadow: var(--app-shadow-primary);
}

.summary-num {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.1;
  color: var(--app-text-1);
}

.summary-label {
  font-size: 12px;
  color: var(--app-text-3);
  margin-top: 2px;
}

.summary-tip {
  margin-left: auto;
  font-size: 11px;
  color: var(--app-text-3);
  padding: 4px 10px;
  border-radius: 999px;
  background-color: rgba(255, 255, 255, 0.7);
}

.favorite-list {
  padding: 14px 12px 0;
}

.favorite-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding: 14px 12px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
  transition: transform 0.28s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.28s ease;
}

.favorite-item:active {
  transform: scale(0.99);
}

@media (hover: hover) {
  .favorite-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--app-shadow-3);
  }
}

.favorite-cell {
  flex: 1;
  min-width: 0;
  padding: 0;
  background: transparent;
}

.favorite-cell :deep(.van-cell__title) {
  padding: 0;
}

.favorite-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.favorite-main {
  flex: 1;
  min-width: 0;
}

.news-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--app-text-1);
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-meta {
  font-size: 12px;
  color: var(--app-text-3);
  display: flex;
  flex-wrap: wrap;
}

.news-meta span + span::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 3px;
  margin: 0 8px;
  border-radius: 50%;
  background-color: #d6d9de;
  vertical-align: middle;
}

.news-favtime {
  margin-top: 8px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 999px;
  background-color: rgba(255, 149, 0, 0.12);
  color: #e8860c;
  font-size: 11px;
}

.news-image {
  width: 108px;
  height: 72px;
  flex-shrink: 0;
  border-radius: var(--app-radius-sm);
  overflow: hidden;
  background: linear-gradient(135deg, #f0f2f6 0%, #e8ebf1 100%);
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.delete-btn {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  min-width: 28px;
  padding: 0;
  border-radius: 50%;
  background-color: rgba(240, 75, 75, 0.1);
  border-color: transparent;
  color: #f04b4b;
  font-size: 13px;
  transition: transform 0.2s ease;
}

.delete-btn:active {
  transform: scale(0.88);
}
</style>
